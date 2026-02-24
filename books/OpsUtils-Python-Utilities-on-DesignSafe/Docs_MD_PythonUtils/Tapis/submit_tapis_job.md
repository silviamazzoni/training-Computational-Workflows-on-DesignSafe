# submit_tapis_job()
***submit_tapis_job(t,job_description,askConfirmJob = True)***

Submit a job to the **Tapis Jobs** service using a prepared job description. By default, the function **prompts for confirmation** to avoid accidental runs. On success, it prints the new **job UUID** and returns a small dictionary with key submission details.

### Parameters

* **t** *(tapipy.tapis.Tapis)* — Authenticated Tapis client.
* **job_description** *(dict)* — The job description (typically built by a helper like *get_tapis_job_description*).
* **askConfirmJob** *(bool, default True)* — Prompt before submitting; set *False* for non‑interactive/batch usage.

### Returns

On success:

```python
{
  'jobUuid': <str>,
  'submitted_job': <object>,
  'job_start_time': <float>,
  'runJobStatus': 'Finished'
}
```

If the submission is **cancelled** (not confirmed):

```python
{'runJobStatus': 'Incomplete'}
```

### Prints

* Submission confirmation/cancellation messages
* The assigned **Tapis job UUID**

### Example

```python
result = submit_tapis_job(t, job_description)
if result.get('runJobStatus') == 'Finished':
    print("Monitor with UUID:", result['jobUuid'])
else:
    print("Submission canceled.")
```


#### Files
You can find these files in Community Data.

```{dropdown} submit_tapis_job.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/submit_tapis_job.py
:language: none
```

