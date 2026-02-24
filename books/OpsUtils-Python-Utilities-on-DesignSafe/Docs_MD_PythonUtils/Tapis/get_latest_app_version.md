# get_latest_app_version()

***get_latest_app_version(t,app_id: str,allow_literal_latest_if_only: bool = True,allow_literal_latest_if_newest: bool = False)***

**Purpose:** Choose a **specific** app version to submit against—even if someone has registered a moving version named ***latest***—while defaulting to **reproducible** behavior.

## How it resolves the version

1. **Ask Tapis for “latest”**

* Calls *t.apps.getAppLatestVersion(appId=...)*.
* If it returns a **concrete** version (e.g., *1.2.3*), that’s returned.
* If it returns the literal ***"latest"***, we *don’t* return it yet; we enumerate versions to pick a reproducible SemVer.

2. **Enumerate all enabled versions**

* Lists enabled versions via *t.apps.getApps(search=..., listType="ALL", select="...")*.
* **If only one enabled version exists and it’s *"latest"*** → return *"latest"* by default (configurable).
* Otherwise, choose the **highest SemVer**:

  * Prefer highest **stable** (no prerelease tag).
  * If none, use highest **prerelease**.

3. **If no SemVer exists at all**

* If a literal *"latest"* is enabled, return it (or, if you set *allow_literal_latest_if_newest=True* and it’s the newest, return it intentionally).

4. **Nothing usable**

* Return *"none"*.

## Parameters

* *t* (*tapipy.tapis.Tapis*): Authenticated client.
* *app_id* (*str*): Application ID (e.g., *opensees-mp-s3*).
* *allow_literal_latest_if_only* (*bool*, default **True**): If *"latest"* is the **only** enabled version, return it; otherwise return *"none"*.
* *allow_literal_latest_if_newest* (*bool*, default **False**): If multiple versions exist and *"latest"* is the **newest**, allow returning *"latest"* (not reproducible).

## Returns

* *str*: A pinned version like *1.2.3*; or *"latest"* per flags/last resort; or *"none"* if no usable version is found.

## Example

```python
app_id = "opensees-mp-s3"

ver = get_latest_app_version(t, app_id)
if ver == "none":
    raise RuntimeError(f"Could not resolve a usable version for {app_id}")

job_req = {
    "name": f"{app_id}-{ver}",
    "appId": app_id,
    "appVersion": ver,
    # ... add your required inputs/params ...
}
resp = t.jobs.submitJob(**job_req)
print("Submitted job:", getattr(getattr(resp, "result", resp), "uuid", "<no-uuid>"))
```

## Notes & best practices

* Defaults **prefer reproducibility**: you’ll get a concrete SemVer whenever possible.
* If your team intentionally relies on a moving *"latest"*, set *allow_literal_latest_if_newest=True* or maintain a pointer file (*apps/<app_id>/latest/version.txt*) with a concrete SemVer and read that first.
* Log the chosen version in your job name and/or echo it in your wrapper for provenance.

