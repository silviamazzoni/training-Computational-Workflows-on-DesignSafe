def validate_app_folder(folder, required_files):
    """
    Validate an app deployment folder:
      1) Check that all `required_files` exist under `folder`.
      2) Parse any `.json` files and merge their objects (later files overwrite earlier keys).
      3) Print a concise summary (id, name, version, params/inputs/outputs, top-level keys).

    Safe behavior:
      - Never raises KeyError for missing identity keys; prints "(missing)" instead.
      - Handles non-list or malformed `parameters/inputs/outputs` gracefully.

    Parameters
    ----------
    folder : str | os.PathLike
        Path to the app/version directory (e.g., "apps/opensees-mp/1.0/").
    required_files : Iterable[str]
        Filenames expected inside `folder` (e.g., ["app.json", "profile.json", "tapisjob_app.sh"]).

    Returns
    -------
    bool
        True  -> all required files present and all JSON parsed successfully.
        False -> at least one file missing OR a JSON parse error occurred.

    Notes
    -----
    - If multiple JSON files are in `required_files`, later files overwrite earlier keys.
    - Only performs **syntactic** JSON validation (no schema validation).
    """
    import os, json
    from pathlib import Path

    folder_path = Path(folder)
    print(f"🔍 Validating app folder: {folder_path}\n")

    # 1) Presence check
    missing = [f for f in required_files if not (folder_path / f).exists()]
    if missing:
        print(f"❌ Missing required files: {missing}")
        return False
    else:
        print("✅ All required files are present.\n")

    # 2) Parse & merge JSON files
    app_def = {}
    for fname in required_files:
        if Path(fname).suffix.lower() == ".json":
            fpath = folder_path / fname
            try:
                with fpath.open() as fp:
                    obj = json.load(fp)
                if isinstance(obj, dict):
                    app_def.update(obj)  # later files override earlier keys
                else:
                    print(f"❌ {fname} contains JSON that is not an object (dict).")
                    return False
            except json.JSONDecodeError as exc:
                print(f"❌ {fname} is not valid JSON: {exc}")
                return False

    # 3) Friendly summary (safe lookups)
    app_id      = app_def.get("id", "(missing)")
    app_name    = app_def.get("name", "(missing)")
    app_version = app_def.get("version", "(missing)")

    def _collect_ids(val, key="id"):
        # Accepts list[dict], dict (single), or anything else -> robust fallback
        if isinstance(val, list):
            return [str(x.get(key, "(no-id)")) for x in val if isinstance(x, dict)]
        if isinstance(val, dict):
            return [str(val.get(key, "(no-id)"))]
        return []

    param_ids  = _collect_ids(app_def.get("parameters", []), "id")
    input_ids  = _collect_ids(app_def.get("inputs", []), "id")
    output_ids = _collect_ids(app_def.get("outputs", []), "id")

    print(f"📄 App ID: {app_id}")
    print(f"📄 App Name: {app_name}")
    print(f"📄 Version: {app_version}")
    print(f"🔧 Parameters: {param_ids}")
    print(f"📦 Inputs: {input_ids}")
    print(f"📤 Outputs: {output_ids}")
    print(f"\nApp Keys: {list(app_def.keys())}")
    print("\n✅ Basic validation complete. App folder looks good!")
    return True
