# get_tapis_app_schema()

***get\_tapis\_app\_schema(t, appId, version='latest', quiet=False)***

Fetch a **Tapis App schema** by ID and version, or grab the **latest** version when you don’t specify one.

## What it does

* Calls *t.apps.getAppLatestVersion(appId=...)* when *version* is empty or *"latest"*.
* Calls *t.apps.getApp(appId=..., appVersion=...)* when you provide a specific version string.
* Returns the schema object (usually a **TapisResult**) or *None* if not found / error.

## Parameters

* *t* *(tapipy.tapis.Tapis)* – Authenticated Tapis client.
* *appId* *(str)* – App ID (e.g., *"opensees-mp-s3"*).
* *version* *(str, default *"latest"*)* – Version string (e.g., *"2.1.0"*) or *"latest"*.
* *quiet* *(bool, default *False*)* – Suppress error prints if *True*.

## Returns

* **App schema** *(TapisResult | dict | None)* – The app schema on success, else *None*.

## Examples

```python
# Latest version
schema = get_tapis_app_schema(t, "opensees-mp-s3")

# Specific version
schema_v = get_tapis_app_schema(t, "opensees-mp-s3", version="2.1.0")

# Quietly attempt
maybe_schema = get_tapis_app_schema(t, "nonexistent-app", quiet=True)
if maybe_schema is None:
    print("Not found.")
```

## Notes

* Uses Tapis Apps service convenience methods for clarity.
* Returns `None` when an app/version isn’t found or other errors occur (printout controlled by `quiet`).

---

#### Files
You can find these files in Community Data.

```{dropdown} get_tapis_app_schema.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/get_tapis_app_schema.py
:language: none
```

