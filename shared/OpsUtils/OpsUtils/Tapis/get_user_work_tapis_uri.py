from __future__ import annotations

from typing import Iterable, Sequence


def get_user_work_tapis_uri(
    t,
    system_id: str = "stampede3",
    *,
    valid_systems: Iterable[str] = ("stampede3", "ls6", "frontera"),
    app_suffix: str = "-credential",
    job_name: str = "getWork",
    tapis_work_system_id: str = "cloud.data",
    work_roots: Sequence[str] = ("work", "work2", "work3", "work4"),
    ensure_trailing_slash: bool = True,
) -> str:
    """
    Return the user's **Work base** as a Tapis URI for the given HPC system.

    The function submits the system's credential app, reads the job's
    `archiveSystemDir` (an HPC filesystem path), extracts the Work root,
    allocation, and system segment, and converts them into a stable Tapis URI:

        tapis://{tapis_work_system_id}/work/{allocation}/{username}/{system_id}/

    Examples
    --------
    archiveSystemDir: /work2/01121/stampede3/home/jdoe/job-abc
    -> tapis://cloud.data/work/01121/jdoe/stampede3/

    Parameters
    ----------
    t : Tapipy client
        Authenticated Tapis v3 client.
    system_id : {"stampede3","ls6","frontera"}
        Target HPC system (case-insensitive).
    valid_systems : Iterable[str]
        Allowed system IDs for validation.
    app_suffix : str
        Suffix for the credential app (default: "-credential"), pattern:
        `{system_id}{app_suffix}`.
    job_name : str
        Name assigned to the temporary credential job.
    tapis_work_system_id : str
        Tapis system ID that fronts the Work storage (DesignSafe: "cloud.data").
    work_roots : Sequence[str]
        Acceptable HPC Work root directory names to detect in archive paths
        (e.g., "work", "work2", ...).
    ensure_trailing_slash : bool
        If True, return URI with a trailing "/" (recommended).

    Returns
    -------
    str
        Tapis URI for the user's Work base on the given system, e.g.:
        "tapis://cloud.data/work/01121/jdoe/stampede3/"

    Raises
    ------
    ValueError
        Unknown system_id, or the expected segments cannot be parsed.
    RuntimeError
        App resolution or job submission failed, or response missing fields.

    Author
    ------
    Silvia Mazzoni, DesignSafe (silviamazzoni@yahoo.com)
    """
    from OpsUtils import OpsUtils
    sys_key = system_id.strip().lower()
    valid = {s.lower() for s in valid_systems}
    if sys_key not in valid:
        raise ValueError(f"Unknown system '{system_id}'. Choose one of: {sorted(valid)}")

    app_id = f"{sys_key}{app_suffix}"

    # Resolve latest app version
    try:
        latest = t.apps.getAppLatestVersion(appId=app_id)
        app_version = getattr(latest, "version", None) or "latest"
    except Exception:
        try:
            app = t.apps.getApp(appId=app_id, appVersion="latest")
            app_version = getattr(app, "version", None) or "latest"
        except Exception as exc2:
            raise RuntimeError(
                f"Could not resolve latest version for appId='{app_id}': {exc2}"
            )

    # Submit temporary credential job
    try:
        submitted_job = t.jobs.submitJob(name=job_name, appId=app_id, appVersion=app_version)
    except Exception as exc:
        raise RuntimeError(
            f"Credential job submission failed for appId='{app_id}', version='{app_version}': {exc}"
        )

    # Extract HPC archive path
    archive_dir = getattr(submitted_job, "archiveSystemDir", None)
    if not archive_dir or not isinstance(archive_dir, str):
        raise RuntimeError("Response missing string field 'archiveSystemDir'.")

    # Parse segments and find: <work_root>/<allocation>/<system_id>
    parts = [p for p in archive_dir.split("/") if p]  # remove empties
    # Find system segment
    try:
        sys_idx = next(i for i, seg in enumerate(parts) if seg.lower() == sys_key)
    except StopIteration:
        raise ValueError(
            f"Expected segment '/{sys_key}' in archiveSystemDir='{archive_dir}', but did not find it."
        )

    # Walk backward to detect the nearest work root before the system segment
    work_idx = None
    for i in range(sys_idx - 1, -1, -1):
        if parts[i].lower() in {r.lower() for r in work_roots}:
            work_idx = i
            break
    if work_idx is None:
        raise ValueError(
            f"Could not identify a Work root ({work_roots}) in '{archive_dir}'."
        )

    alloc_idx = work_idx + 1
    if alloc_idx >= sys_idx:
        raise ValueError(
            f"Could not locate allocation segment between '{parts[work_idx]}' and '{parts[sys_idx]}' in '{archive_dir}'."
        )

    allocation = parts[alloc_idx]
    try:
        username = OpsUtils.get_tapis_username(t)
    except Exception as e:
        raise RuntimeError(f"Could not determine Tapis username: {e}")

    # Build Tapis URI
    uri = f"tapis://{tapis_work_system_id}/work/{allocation}/{username}/{sys_key}/"
    if not ensure_trailing_slash:
        uri = uri.rstrip("/")
    return uri