# cancel_tapis_job()
***cancel_tapis_job(tapis_client, job_uuid)***

** Cancel a Tapis Job with Robust Error Handling** 

Here's an enhanced and more **robust version** of the *tapipy* job cancellation snippet, including:

* Error handling,
* Status confirmation,
* Optional retry messaging for common user mistakes (e.g., invalid UUID, already finished jobs),
* And a clean function you can reuse in your codebase or Jupyter workflows.

---

### Example Usage

```python
from tapipy.tapis import Tapis

# Assume you already have an authenticated client
# t = Tapis(base_url='https://tacc.tapis.io', access_token='your_token_here')

job_id = 'abc123-your-job-uuid'
cancel_tapis_job(t, job_id)
```

---

### Tip: When Jobs Can't Be Cancelled

Some jobs may already be in a terminal state (*FINISHED*, *FAILED*, *CANCELLED*) and cannot be stopped. You can pre-check status like this:

```python
status = t.jobs.getJob(jobId=job_id).status
if status in ['FINISHED', 'FAILED', 'CANCELLED']:
    print(f"Job is already in a terminal state: {status}")
else:
    cancel_tapis_job(t, job_id)
```



#### Files
You can find these files in Community Data.

```{dropdown} cancel_tapis_job.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/cancel_tapis_job.py
:language: none
```

