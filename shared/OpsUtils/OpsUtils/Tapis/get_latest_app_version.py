def get_latest_app_version(
    t,
    app_id: str,
    allow_literal_latest_if_only: bool = True,
    allow_literal_latest_if_newest: bool = False,
) -> str:
    """
    Resolve a concrete app version for `app_id`, robust to Tapipy resource objects
    vs dicts, and to a version literally named "latest".

    Resolution order (defaults favor reproducibility):
      1) Try Apps helper getAppLatestVersion:
         - If it returns a concrete version (not "latest"), return it.
         - If it returns "latest", enumerate all versions (step 2).
      2) Enumerate enabled versions via getApps(search=...):
         - If "latest" is the ONLY enabled version → return "latest"
           (controlled by allow_literal_latest_if_only; default True).
         - Otherwise pick highest semantic version (SemVer):
             * Prefer highest stable; if none, highest prerelease.
         - If no SemVer and `allow_literal_latest_if_newest` is True and the newest
           record is "latest", return "latest" (NOT reproducible).
      3) If no SemVer at all but a literal "latest" exists → return "latest".
      4) Otherwise → return "none".

    Parameters
    ----------
    t : tapipy.tapis.Tapis
        Authenticated Tapis client.
    app_id : str
        Application identifier (e.g., "opensees-mp-s3").
    allow_literal_latest_if_only : bool, default True
        If True and "latest" is the only enabled version, return "latest".
        If False, return "none" in that scenario.
    allow_literal_latest_if_newest : bool, default False
        If True and "latest" is the most recently created among multiple versions,
        allow returning "latest" instead of a pinned SemVer (NOT reproducible).

    Returns
    -------
    str
        Concrete version like "1.2.3", or "latest" (per flags/last resort), or "none".

    Notes
    -----
    - Defaults keep jobs reproducible by preferring a concrete SemVer.
    - Consider maintaining `apps/<app_id>/latest/version.txt` with a SemVer to
      avoid returning a moving "latest".

    Examples
    --------
    >>> ver = get_latest_app_version(t, "opensees-mp-s3")
    >>> if ver not in ("none", "latest"):
    ...     t.jobs.submitJob(name=f"opensees-mp-{ver}", appId="opensees-mp-s3", appVersion=ver)

    Author
    ------
    Silvia Mazzoni, DesignSafe (silviamazzoni@yahoo.com)
    Date
    ----
    2025-08-16
    Version
    -------
    1.5
    """
    from typing import Any, List, Tuple
    from packaging.version import Version
    def _field(obj: Any, name: str, default=None):
        # Works for Tapipy Resource objects and dicts
        if isinstance(obj, dict):
            return obj.get(name, default)
        return getattr(obj, name, default)

    # 1) Try official "latest" helper
    try:
        # print('try')
        latest = t.apps.getAppLatestVersion(appId=app_id)
        # print('latest',latest)
        latest = getattr(latest, "result", latest)
        v = _field(latest, "version")
        # print('v',v)
        if isinstance(v, str) and v:
            if v.lower() != "latest":
                return v  # concrete version resolved by the service
            # literal "latest" → enumerate for reproducible SemVer
    except Exception:
        pass

    # 2) Enumerate all enabled versions
    try:
        resp = t.apps.getApps(
            search=f"(id.eq.{app_id})",
            listType="ALL",
            select="id,version,enabled,versionEnabled,created",
        )
        items = getattr(resp, "result", resp)
        if not isinstance(items, list):
            items = [items] if items else []

        # Filter enabled (either/both flags may exist)
        enabled: List[Any] = []
        for it in items:
            en = bool(_field(it, "enabled", True))
            ven = bool(_field(it, "versionEnabled", True))
            if en and ven:
                enabled.append(it)

        if not enabled:
            return "none"

        # Only one enabled?
        if len(enabled) == 1:
            v = (_field(enabled[0], "version", "") or "").strip()
            if v.lower() == "latest":
                return "latest" if allow_literal_latest_if_only else "none"
            return v if v else "none"

        # Multiple enabled → metadata
        def created_key(u):
            return _field(u, "created", "") or ""

        literal_latest_records = [
            it for it in enabled
            if isinstance(_field(it, "version", ""), str)
            and _field(it, "version", "").lower() == "latest"
        ]
        has_literal_latest = len(literal_latest_records) > 0

        newest = max(enabled, key=created_key) if enabled else None
        newest_is_literal_latest = bool(
            newest and isinstance(_field(newest, "version", ""), str)
            and _field(newest, "version", "").lower() == "latest"
        )

        # Build SemVer sets
        stable: List[Tuple[Version, str]] = []
        prerelease: List[Tuple[Version, str]] = []
        for it in enabled:
            v = (_field(it, "version", "") or "").strip()
            if not v or v.lower() == "latest":
                continue
            try:
                sv = Version(v)
                (stable if not sv.is_prerelease else prerelease).append((sv, v))
            except Exception:
                # Skip non-SemVer strings
                continue

        if stable:
            stable.sort(key=lambda x: x[0])
            return stable[-1][1]
        if prerelease:
            prerelease.sort(key=lambda x: x[0])
            return prerelease[-1][1]

        # No SemVer available
        if has_literal_latest:
            if newest_is_literal_latest and allow_literal_latest_if_newest:
                return "latest"
            return "latest"  # last resort to preserve functionality

        return "none"

    except Exception:
        return "none"

