# get_tapis_job_status()

***get_tapis_job_status(t, jobUuid, print_all=True, return_values=False)***

Retrieve and optionally display the status of a Tapis job in a Jupyter-friendly format.

By default, this function shows the status in an **accordion widget** with:
- The job's UUID  
- The raw *TapisResult* status object  
- An optional *message* field from the Tapis status  
- Any error messages found in the job history  

If desired, the raw status object can be returned for further programmatic use.

---

**Inputs:**

* **t** (*Tapis client object*):  
  Authenticated Tapis client instance (e.g., from `tapis3` or `py-tapis`).

* **jobUuid** (*str*):  
  UUID of the Tapis job to query.

* **print_all** (*bool*, optional):  
  If **True** (default), prints and displays the job status in a Jupyter accordion widget.  
  If **False**, suppresses all output.

* **return_values** (*bool*, optional):  
  If **True**, returns the `TapisResult` object containing job status.  
  If **False** (default), returns `None`.

---

**Outputs:**

* If *return_values=True* — returns a *TapisResult* object containing job status fields from Tapis.
* If *return_values=False* — returns *None*.

---

**Behavior:**

1. Queries the Tapis Jobs service for the specified job’s status.
2. Optionally displays job details in a structured, collapsible widget.
3. If available, includes any error messages from the job history.

---

**Example usage:**

```python
get_tapis_job_status(t, "1234-uuid-5678")

# With return value
status = get_tapis_job_status(t, "1234-uuid-5678", return_values=True)
print(status.status)
````

**Sample output in notebook:**

```
++++++++++++++++++++++++++++++
++++++ Job Status ++++++
++++++++++++++++++++++++++++++
jobUuid: 1234-uuid-5678
Job Status: TapisResult(...)
++++++++++++++++++++++++++++++
message: Job completed successfully
++++++++++++++++++++++++++++++
```

---


#### Files
You can find these files in Community Data.

```{dropdown} get_tapis_job_status.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/get_tapis_job_status.py
:language: none
```

