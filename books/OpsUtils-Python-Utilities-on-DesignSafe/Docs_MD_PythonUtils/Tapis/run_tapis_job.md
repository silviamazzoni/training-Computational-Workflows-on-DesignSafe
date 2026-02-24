# run_tapis_job()

***run_tapis_job(t, tapisInput, askConfirmJob=True, monitor_job=True, askConfirmMonitorRT=True,
get_job_history=False, get_job_metadata=False, get_job_filedata=False, job_description={})***

A convenience wrapper that submits a **Tapis job** and, if requested, **monitors** it and gathers
**status / metadata / history / file data** — all in one call.

## What it does

1. **Job description**
   - If *job_description* (dict) is provided, it is used as-is.
   - Otherwise, one is built from *tapisInput* via *OpsUtils.get_tapis_job_description*.

2. **Submit**
   - Submits with *OpsUtils.submit_tapis_job* (optional confirmation).

3. **Monitor (optional)**
   - If *monitor_job=True*:
     - Monitors runtime with *OpsUtils.monitor_tapis_job*.
     - Always fetches **basic status** via *OpsUtils.get_tapis_job_status*.
     - If *get_job_metadata=True*, fetches **detailed metadata** via *OpsUtils.get_tapis_job_metadata*.
     - If *get_job_history=True*, fetches **history** via *OpsUtils.get_tapis_job_history_data*.
     - If *get_job_filedata=True*, fetches **output file data** via *OpsUtils.get_tapis_job_all_files*.

## Parameters

- *t* *(tapipy.tapis.Tapis)* — Authenticated Tapis client.  
- *tapisInput* *(dict)* — Used to build the job description when *job_description* is not provided.  
- *askConfirmJob* *(bool, default True)* — Ask before submitting.  
- *monitor_job* *(bool, default True)* — Monitor the job in real time (required for downstream fetches).  
- *askConfirmMonitorRT* *(bool, default True)* — Ask before starting monitoring.  
- *get_job_history* *(bool, default False)* — Include job history (requires *monitor_job=True*).  
- *get_job_metadata* *(bool, default False)* — Include detailed metadata (requires *monitor_job=True*).  
- *get_job_filedata* *(bool, default False)* — Include output file listings/data (requires *monitor_job=True*).  
- *job_description* *(dict, default {})* — Optional pre-built job request that **overrides** building from *tapisInput*.

## Returns

A dictionary seeded from *OpsUtils.submit_tapis_job(...)*, augmented with:

```python
{
  "runJobStatus":   "Finished" | "Incomplete" | ...,
  "jobUuid":        "...",                  # from submission helper
  "job_start_time": <float>,                # from submission helper
  "job_description": <dict>,                # built or provided
  "JobMetadata":     <dict or {}>,          # status or detailed metadata
  "JobHistory":      <dict or {}>,          # if requested
  "JobFiledata":     <dict or {}>,          # if requested
}
```

If building the job description fails, returns *{"runJobStatus": "Incomplete"}*.

## Example

```python
result = run_tapis_job(
    t, tapisInput,
    monitor_job=True,
    get_job_history=True,
    get_job_metadata=True,
    get_job_filedata=False
)
print("UUID:",   result.get("jobUuid"))
print("Status:", result.get("JobMetadata", {}).get("status"))
```

## Notes

* Status/metadata/history/file data are gathered **only** when *monitor_job=True*.
* If *OpsUtils.submit_tapis_job* returns a non-*Finished* status, that object is returned unchanged
  (except the early *{"runJobStatus":"Incomplete"}* short-circuit).

---

**Author:** Silvia Mazzoni, DesignSafe ([silviamazzoni@yahoo.com](mailto:silviamazzoni@yahoo.com))
**Date:** 2025-08-16
**Version:** 1.1

#### Files

You can find these files in Community Data.

````{dropdown} run_tapis_job.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/run_tapis_job.py
:language: none
````

```
::contentReference[oaicite:0]{index=0}
```
