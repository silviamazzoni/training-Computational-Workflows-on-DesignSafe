# get_user_work_tapis_uri()
***def get_user_path_tapis_uri(t,file_system: str = "none",paths_file_path: str = "~/MyData/.tapis_user_paths.json",force_refresh: bool = False)***



## Purpose

Return the user’s **Work base** as a **Tapis URI** for a given HPC system (e.g., *stampede3*, *ls6*, *frontera*). The function submits the system’s **credential app**, reads the job’s *archiveSystemDir* (an HPC filesystem path), and constructs a Tapis URI by taking the path prefix up to the system name and converting it to:

```
tapis://<tapis_work_system_id>/<work-prefix>/<system_id>[/]
```

* By default there’s **no trailing slash**; set *ensure_trailing_slash=True* to include it.
* The default Tapis Work system on DesignSafe is ***cloud.data***.

#### Signature

```python
get_user_work_tapis_uri(
    t,
    system_id: str = "stampede3",
    *,
    valid_systems: Iterable[str] = ("stampede3", "ls6", "frontera"),
    tapis_work_system_id: str = "cloud.data",
    app_suffix: str = "-credential",
    job_name: str = "getWork",
    ensure_trailing_slash: bool = False,
) -> str
```

#### Parameters

* **t** — authenticated Tapipy v3 client.
* **system\_id** — target HPC system (*"stampede3"*, *"ls6"*, *"frontera"*).
* **valid\_systems** — allowed system IDs for validation.
* **tapis\_work\_system\_id** — Tapis system that fronts Work (DesignSafe: *"cloud.data"*).
* **app\_suffix** — suffix for the credential app ID (*"{system_id}{app_suffix}"*).
* **job\_name** — name for the short-lived credential job.
* **ensure\_trailing\_slash** — append a */* at the end of the returned URI (handy for simple string joins).

#### Returns

A **string** Tapis URI representing the user’s Work base for the given system, for example:

```
tapis://cloud.data/work2/01121/jdoe/stampede3/
```

*(trailing slash present only if *ensure_trailing_slash=True*)*

#### Raises

* **ValueError** — unknown *system_id*.
* **RuntimeError** — app version resolution, job submission, or response fields are missing/invalid.

#### Example

```python
uri = get_user_work_tapis_uri(t, system_id="stampede3", ensure_trailing_slash=True)
# e.g., "tapis://cloud.data/work2/01121/jdoe/stampede3/"
inputs = uri + "inputs/model.tcl"
outputs = uri + "outputs/run01/"
```

> Tip: Run this once per system and **cache** the resulting base URIs (e.g., in *~/.tapis_user_paths.json*) for reuse across notebooks and job submissions.

#### Files
You can find these files in Community Data.

```{dropdown} get_user_work_tapis_uri.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/get_user_work_tapis_uri.py
:language: none
```

