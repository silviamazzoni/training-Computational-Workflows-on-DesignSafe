# explore_tapis_job()
***explore_tapis_job(t, jobUuid)***

Explore a Tapis job end‑to‑end: prints **job name**, **status**, a formatted **history**, and lists the **outputs** (including the *inputDirectory* subtree when present). In Jupyter notebooks with *ipywidgets* installed, it also shows a simple **dropdown** to pick a file for download.

## What it does

* Fetches and prints **job metadata** (name) and **status**.
* Calls your existing *OpsUtils.process_tacc_job_history* to print a readable **history**.
* Lists **outputs** at "." and, if present, under "./inputDirectory".
* Returns a **structured dictionary** with everything it discovered.

## Signature

```python
explore_tapis_job(t, jobUuid)
```

## Parameters

* **t** *(tapipy.tapis.Tapis)* — Authenticated Tapis client.
* **jobUuid** *(str)* — Job UUID to explore.

## Returns

```python
{
  "jobUuid": str,
  "name": str | None,
  "status": str | None,
  "outputs": [{"path": str, "type": str}, ...],
  "inputDirectoryOutputs": [{"path": str, "type": str}, ...],
  "timestamp": str,  # UTC ISO8601
}
```

## Example

```python
info = explore_tapis_job(t, "1b2c3d4e-...-...-...")
print("Status:", info["status"])
print("First 3 outputs:", info["outputs"][:3])
```

## Notes

* If *ipywidgets* isn’t available, the function still prints and returns data; it just skips the dropdown.
* If *OpsUtils.process_tacc_job_history* isn’t importable, the function warns and continues.


---

#### Files

You can find these files in Community Data.

````{dropdown} explore_tapis_job.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/explore_tapis_job.py
:language: none
````








