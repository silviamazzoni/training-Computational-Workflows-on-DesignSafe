# get_tapis_job_description()

***get_tapis_job_description(t, tapisInput)***

Generate a complete **Tapis v3 job description** from a concise input dict. The helper:

1. **Resolves input baseURL**
   - If *storage_system_baseURL* is missing, it is derived from *storage_system*:
     - *"mydata"*    → *tapis://designsafe.storage.default/<username>*
     - *"community"* → *tapis://designsafe.storage.community*
     - *"published"* → *tapis://designsafe.storage.published*
   - The final *sourceUrl* used in *fileInputs* is: *"<baseURL>/<input_folder>"*.

2. **Ensures a concrete appVersion**
   - If *appVersion* is missing **or** equals *"latest"*, the function resolves a **pinned** version via *OpsUtils.get_latest_app_version(t, <appId>)*.
   - If it cannot resolve, the function returns *-1* with a helpful message.

3. **Validates inputs**
   - **OpenSees-Express** (*appId == "opensees-express"*; defaults *execSystemId* to *wma-exec-01* if not given):
     Required:
     *['name','appId','appVersion','maxMinutes','archive_system',
       'storage_system','input_folder','input_filename']*
   - **HPC OpenSees apps** (e.g., *opensees-mp-s3*, SP variants):
     Required:
     *['name','appId','appVersion','execSystemId','execSystemLogicalQueue',
       'nodeCount','coresPerNode','maxMinutes','allocation','archive_system',
       'storage_system','input_folder','input_filename']*

4. **Assembles the job description**
   - **Express (Tcl)**
     - *parameterSet.envVariables = [{"key":"mainProgram","value":"OpenSees"},
                                     {"key":"tclScript","value": <input_filename>}]*
     - *fileInputs = [{"name":"Input Directory","sourceUrl": <base>/<input_folder>}]*
   - **HPC (MP/SP)**
     - Base job attributes: system, queue, resources, app id/version.
     - *parameterSet.appArgs = [{"name":"Main Script","arg": <input_filename>}]*
     - *parameterSet.schedulerOptions = [{"name":"TACC Allocation","arg": f"-A {allocation}"}]*
     - *fileInputs* as above.

5. **Archive location**
   - **Express**
     - *archive_system == 'MyData'* → *designsafe.storage.default:${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}*
     - *archive_system == 'Temp'*   → *cloud.data:/tmp/${JobOwner}/tapis-jobs-archive/${JobCreateDate}/${JobName}-${JobUUID}*
   - **HPC (MP/SP)**
     - *archive_system == 'MyData'* → same as above (MyData path)
     - *archive_system == 'Work'*   → *${WORK}/tapis-jobs-archive/${JobCreateDate}/${JobName}-${JobUUID}* on the **execution system**

## Parameters

- *t* *(tapipy.tapis.Tapis)* — Authenticated client (discovers username for MyData).
- *tapisInput* *(dict)* — See required keys above; optionally include
  *storage_system_baseURL* to bypass auto-detection.

## Returns

- **dict** — Ready-to-submit Tapis job description.  
- **-1** — Validation failed, or baseURL/appVersion could not be determined.

Also prints missing keys (if any) and a confirmation message when inputs are complete.

## Examples

### OpenSees-Express (MyData inputs; auto-resolve appVersion)
```python
tapisInput = {
  "name": "opensees-express-smoke",
  "appId": "opensees-express",
  # "appVersion": "latest",  # optional; can omit or set "latest" to auto-resolve
  "maxMinutes": 10,
  "archive_system": "MyData",
  "storage_system": "MyData",
  "input_folder": "projects/demo/input",
  "input_filename": "model.tcl"
}
desc = get_tapis_job_description(t, tapisInput)
````

### OpenSeesMP on Stampede3 (community inputs; pinned appVersion)

```python
tapisInput = {
  "name": "opensees-mp-smoke",
  "appId": "opensees-mp-s3",
  "appVersion": "1.0.0",
  "execSystemId": "designsafe.community.stampede3",
  "execSystemLogicalQueue": "normal",
  "nodeCount": 1,
  "coresPerNode": 56,
  "maxMinutes": 10,
  "allocation": "TACC-XYZ123",
  "archive_system": "Work",
  "storage_system": "community",
  "input_folder": "training/opensees/examples",
  "input_filename": "model.tcl"
}
desc = get_tapis_job_description(t, tapisInput)
```

## Notes

* *fileInputs* uses the **tapis\://** scheme; the platform will stage inputs from that system/path.
* For **MyData** auto-detection, the function queries your Tapis userinfo to insert your username.
* The function resolves and **pins** *appVersion* when you omit it or set *"latest"*.
* Returns **-1** if anything essential is missing; the console lists missing keys.

---

**Author:** Silvia Mazzoni, DesignSafe ([silviamazzoni@yahoo.com](mailto:silviamazzoni@yahoo.com))
**Date:** 2025-08-16
**Version:** 1.2

#### Files

You can find these files in Community Data.

````{dropdown} get_tapis_job_description.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/get_tapis_job_description.py
:language: none
```
````
