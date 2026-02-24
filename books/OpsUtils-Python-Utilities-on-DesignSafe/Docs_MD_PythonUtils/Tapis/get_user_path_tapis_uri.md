# get_user_path_tapis_uri()

***get_user_work_tapis_uri(    t,
    system_id: str = "stampede3",
    *,
    valid_systems: Iterable[str] = ("stampede3", "ls6", "frontera"),
    tapis_work_system_id: str = "cloud.data",
    app_suffix: str = "-credential",
    job_name: str = "getWork",
    ensure_trailing_slash: bool = False,) -> Path***


Discover and cache your **Tapis base URIs** for DesignSafe storage systems, then return either the **entire dictionary** or a **single base** by key.

This function writes/reads a JSON cache (default: `~/MyData/.tapis_user_paths.json`) so you only have to discover paths once. Subsequent calls are instant unless you pass `force_refresh=True`.

#### What it returns

A mapping like:

```json
{
  "mydata":    "tapis://designsafe.storage.default/<username>/",
  "community": "tapis://designsafe.storage.community/",
  "published": "tapis://designsafe.storage.published/",
  "work/stampede3": "tapis://cloud.data/work/<alloc>/<username>/stampede3/",
  "work/ls6":       "tapis://cloud.data/work/<alloc>/<username>/ls6/",
  "work/frontera":  "tapis://cloud.data/work/<alloc>/<username>/frontera/"
}
```

> All URIs are normalized to start with `tapis://` and include a trailing `/`.

#### Signature

```python
get_user_path_tapis_uri(
    t,
    file_system: str = "none",                  # "none" | "mydata" | "community" | "published" | "work/<system>"
    paths_file_path: str = "~/MyData/.tapis_user_paths.json",
    force_refresh: bool = False,
) -> Union[str, Dict]
```

#### Parameters

* **t** — authenticated Tapipy v3 client.
* **file\_system** — key to return:

  * `"none"` → return the full dictionary
  * `"mydata"`, `"community"`, `"published"` → return that base
  * `"work/stampede3"`, `"work/ls6"`, `"work/frontera"` → return that Work base
* **paths\_file\_path** — JSON cache file path (defaults to **MyData**).
* **force\_refresh** — rediscover bases and overwrite the cache.

#### How discovery works

* **MyData** → `designsafe.storage.default/<username>`
* **Community** → `designsafe.storage.community`
* **Published** → `designsafe.storage.published`
* **Work/\*** → calls `OpsUtils.get_user_work_tapis_uri(t, system_id=...)` for each system and stores the returned URI.

#### Examples

```python
# 1) Get everything (and write cache if missing)
paths = get_user_path_tapis_uri(t)

# 2) Just MyData base
mydata_base = get_user_path_tapis_uri(t, "mydata")

# 3) Work base for Stampede3
s3_base = get_user_path_tapis_uri(t, "work/stampede3")

# 4) Force refresh (e.g., after allocation changes)
paths = get_user_path_tapis_uri(t, force_refresh=True)
```

#### Errors & troubleshooting

* **ValueError** — `file_system` not in the accepted set:

  * `{"none","mydata","community","published","work/stampede3","work/ls6","work/frontera","work/none"}`
* **RuntimeError** — could not determine username; or a Work base couldn’t be discovered by `OpsUtils.get_user_work_tapis_uri`.

> Tip: Run once at the start of your workflow to populate the cache for all systems you use. Then reference by key (`"mydata"`, `"work/stampede3"`, etc.) throughout your notebooks and submission scripts.




#### Files
You can find these files in Community Data.

```{dropdown} get_user_path_tapis_uri.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/get_user_path_tapis_uri.py
:language: none
```

