from __future__ import annotations

def get_user_path_tapis_uri(
    t,
    file_system: str = "none",                  # "none" | "mydata" | "community" | "work/stampede3","work/ls6","work/frontera"

    paths_file_path: str = "~/MyData/.tapis_user_paths.json",
    force_refresh: bool = False,
) -> Union[str, Dict]:
    """
    Discover and cache user-specific Tapis base URIs for DesignSafe storage systems,
    then return either the entire dictionary or a single base URI.

    Author
    -------
    Silvia Mazzoni, DesignSafe (silviamazzoni@yahoo.com)

    Parameters
    ----------
    t : Tapipy client
        An authenticated Tapipy v3 client.
    file_system : {"none","mydata","community","work"}, optional
        Which base to return. Use "none" to return the full dictionary.
        When file_system="work", which HPC system's Work base to return.
    paths_file_path : str, optional
        Location (on MyData or local home) where the JSON cache is stored.
        Default: "~/MyData/.tapis_user_paths.json".
    force_refresh : bool, optional
        If True, (re)discover all bases and overwrite the cache file.

    Returns
    -------
    Union[str, dict]
        - If file_system == "none": the full dict of bases (including subdict for "work").
        - Else: a single base URI string for the requested system.

    Notes
    -----
    - Stored values are full Tapis URIs (start with "tapis://" and end with "/").
    - Keys are lowercase: "mydata", "community", "work". For "work", values are a dict
      keyed by HPC system ("stampede3", "ls6", "frontera").
    """
    import json
    import os
    from pathlib import Path
    from typing import Dict, Optional, Union, Iterable, Sequence
    from OpsUtils import OpsUtils

    # ----------------------------
    # normalize & validate inputs
    # ----------------------------
    fs = (file_system or "none").strip().lower()
    # print('fs',fs)

    # Handle loose input like "CommunityData"
    if "community" in fs:
        fs = "community"

    valid_file_systems = ["mydata", "community",  "published","none"]
    valid_work_systems = ["stampede3", "ls6", "frontera", "none"]
    for thisW in valid_work_systems:
        valid_file_systems.append(f'work/{thisW}')
    # print('valid_file_systems',valid_file_systems)

    if fs not in valid_file_systems:
        raise ValueError(f"file_system='{file_system}' not in {sorted(valid_file_systems)}")

    cache_path = Path(os.path.expanduser(paths_file_path))
    # print('cache_path',cache_path)

    # ----------------------------
    # helper: normalize URIs
    # ----------------------------
    def _with_scheme(u: str) -> str:
        u = u.strip()
        if not u:
            return u
        if not u.startswith("tapis://"):
            u = "tapis://" + u.lstrip("/")
        # if not u.endswith("/"):
        #     u += "/"
        u = u.rstrip("/")
        return u

    # ----------------------------
    # try reading existing cache
    # ----------------------------
    paths: Dict = {}
    if cache_path.exists() and not force_refresh:
        try:
            with cache_path.open("r", encoding="utf-8") as f:
                paths = json.load(f)
                print(f'found paths file: {cache_path}')
        except Exception:
            paths = {}
            
    # quick return if cache satisfies the request
    def _maybe_return_from_cache() -> Optional[Union[str, Dict]]:
        if not paths:
            return None
        if fs == "none":
            return paths
        if fs in {"mydata", "community", "published"}:
            val = paths.get(fs)
            if isinstance(val, str) and val:
                return _with_scheme(val)
        if "work" in fs:
            val = paths.get(fs)
            if isinstance(val, str) and val:
                return _with_scheme(val)
        return None

    cached = _maybe_return_from_cache()
    if cached is not None:
        return cached

    # ----------------------------
    # (re)discover all bases
    # ----------------------------
    try:
        username = OpsUtils.get_tapis_username(t)
    except Exception as e:
        raise RuntimeError(f"Could not determine Tapis username: {e}")

    discovered: Dict = {
        "mydata": _with_scheme(f"designsafe.storage.default/{username}"),
        "community": _with_scheme("designsafe.storage.community"),
        "published": _with_scheme("designsafe.storage.published"),
    }

    # Discover Work bases using the new inner helper
    for system in ("stampede3", "ls6", "frontera"):
        try:
            base_uri = OpsUtils.get_user_work_tapis_uri(t, system_id=system)
            discovered[f'work/{system}'] = _with_scheme(base_uri)  # idempotent
        except Exception:
            # Skip systems we can't resolve; they can be refreshed later
            continue

    # Persist to cache

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with cache_path.open("w", encoding="utf-8") as f:
        json.dump(discovered, f, indent=2)
        print(f'saved data to {cache_path}')

    # Return per request
    if fs == "none":
        return discovered
    else:
        return discovered[fs]

    return discovered
