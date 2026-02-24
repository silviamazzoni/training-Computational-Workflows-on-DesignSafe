# validate_app_folder()
***validate_app_folder(folder, required_files)***

**Purpose:** Sanity-check an app deployment folder before registration. Confirms **files exist**, **JSON parses**, and prints a compact **summary**—without throwing `KeyError` if some identity fields are missing.

## What it does

1. **File existence**
   Verifies each entry in `required_files` exists under `folder`.
   → Missing list is printed; returns **False**.

2. **JSON validity & merge**
   Parses every `*.json` file and merges objects into a single dict (`dict.update` → later files overwrite earlier keys).
   → Any parse error or non-object JSON prints a clear message; returns **False**.

3. **Friendly summary (safe lookups)**
   Prints:

   * **App ID / Name / Version** — missing fields show as `"(missing)"` (no exceptions).
   * **Parameters / Inputs / Outputs** — prints their `id` values if present; handles list or dict forms.
   * **Top-level keys** detected in the merged JSON.
     → Returns **True** on success.

## Signature

```python
validate_app_folder(folder, required_files) -> bool
```

**Parameters**

* `folder` (`str | os.PathLike`): Path to the version directory (e.g., `apps/opensees-mp/1.0/`).
* `required_files` (`Iterable[str]`): Expected filenames (e.g., `["app.json","profile.json","tapisjob_app.sh"]`).

**Returns**

* `True` — all files present and JSON valid.
* `False` — a file is missing or a JSON file is invalid.

## Notes & tips

* **No KeyError:** Identity fields (`id`, `name`, `version`) are printed using `.get(...)`, so missing fields don’t crash validation.
* **Overwrite rule:** If multiple JSON files define the same key, the **last one wins**. Keep identity fields in a single source of truth (usually `app.json`).
* **Schema checks:** This is **syntactic** validation. If you want to enforce required keys/structures, add a JSON Schema step later in your pipeline.

## Example

```python
required = ["app.json", "profile.json", "tapisjob_app.sh"]
if not validate_app_folder("./apps/opensees-mp/1.0", required):
    print("Fix the issues above and try again.")
```




### Files
You can find these files in Community Data.

```{dropdown} validate_app_folder.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/validate_app_folder.py
:language: none
```
