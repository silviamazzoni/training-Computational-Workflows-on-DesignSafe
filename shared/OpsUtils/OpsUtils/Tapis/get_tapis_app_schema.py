def get_tapis_app_schema(t, appId: str, version: str = "latest", quiet: bool = False):
    """
    Fetch a Tapis App schema by ID and version (or the latest version).

    Behavior
    --------
    - If `version` is empty or equals "latest" (case-insensitive), retrieves the app's
      latest available version via `t.apps.getAppLatestVersion`.
    - Otherwise, retrieves the specified version via `t.apps.getApp(appVersion=...)`.
    - Returns the schema object (typically a TapisResult) on success, `None` on failure.

    Parameters
    ----------
    t : tapipy.tapis.Tapis
        An authenticated Tapis client.
    appId : str
        The Tapis app ID (e.g., "opensees-mp-s3").
    version : str, default "latest"
        App version string (e.g., "1.0.3") or "latest" (case-insensitive).
    quiet : bool, default False
        If True, suppresses error prints and simply returns `None` on failure.

    Returns
    -------
    tapipy.tapis.TapisResult | dict | None
        The app schema object on success (commonly a TapisResult). Returns `None` when
        not found or if an error occurs.

    Example
    -------
    # Get latest
    schema = get_tapis_app_schema(t, "opensees-mp-s3")
    # Get a specific version
    schema_v = get_tapis_app_schema(t, "opensees-mp-s3", version="2.1.0")

    Author
    ------
    Silvia Mazzoni, DesignSafe (silviamazzoni@yahoo.com)

    Date
    ----
    2025-08-14

    Version
    -------
    1.0
    """
    from tapipy.errors import BaseTapyException

    # Normalize version
    ver = (version or "").strip().lower()

    try:
        if ver == "" or ver == "latest":
            return t.apps.getAppLatestVersion(appId=appId)
        else:
            return t.apps.getApp(appId=appId, appVersion=version)
    except BaseTapyException as e:
        if not quiet:
            print(f"I was unable to find Tapis app: '{appId}', version='{version}'. Error: {e}")
        return None
    except Exception as e:
        if not quiet:
            print(f"Unexpected error retrieving app '{appId}' (version='{version}'): {e}")
        return None
