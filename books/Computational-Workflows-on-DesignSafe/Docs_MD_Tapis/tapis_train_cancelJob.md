# Cancel Tapis Job
**how to stop jobs using Tapis, specifically with the Python client *tapipy***

Once you've submitted a job using Tapis, you may need to **stop or cancel** it—for example, if you detect a mistake in the input, want to halt a long-running job, or need to resubmit with different parameters. Tapis provides the ability to **cancel a job that is queued or currently running**.

**NOTE**: This page is **not** an interactive Jupyter Notebook. 


## How to Cancel a Job (Recommended Approach)
If you need to cancel a job, the quickest and safest method is often to do it manually through the [DesignSafe Job Management page](https://www.designsafe-ci.org/workspace/history). Using the web portal reduces the chance of errors and provides immediate visual confirmation that the job has been cancelled.


## Stopping a Job via CLI

If you're using the Tapis CLI, you can cancel a job using the following command:

```bash
tapis jobs cancel $JOB_UUID
```

Replace *$JOB_UUID* with the actual UUID of your submitted job.



## Stopping a Job Using *tapipy*

To stop (cancel) a job programmatically using Python and the *tapipy* client, use the *cancelJob()* method on the *jobs* service. Here's a simple example:

```python
# Assuming *t* is your authenticated Tapis client
job_uuid = 'your-job-uuid-here'

# Cancel the job
t.jobs.cancelJob(jobId=job_uuid)
print(f"Job {job_uuid} has been cancelled.")
```

### Notes:

* The job must be in a *PENDING*, *PROCESSING_INPUTS*, or *RUNNING* state for the cancel operation to succeed.
* Canceling a job will attempt to terminate the corresponding job on the execution system (e.g., Stampede3 or Frontera), and it will no longer produce output.



## Monitoring Cancellations

After calling *cancelJob*, you can monitor the job’s status using:

```python
job_status = t.jobs.getJob(jobId=job_uuid).status
print(f"Current job status: {job_status}")
```

Once canceled, the job's final status will typically show as *CANCELLED*.



## When to Use This

Use job cancellation when:

* You submitted incorrect inputs.
* The job is taking too long due to misconfiguration.
* You want to free up resources for another run.
* You are debugging or testing job workflows.



## Tip: When Jobs Can't Be Cancelled

Some jobs may already be in a terminal state (*FINISHED*, *FAILED*, *CANCELLED*) and cannot be stopped. You can pre-check status like this:

```python
status = t.jobs.getJob(jobId=job_id).status
if status in ['FINISHED', 'FAILED', 'CANCELLED']:
    print(f"Job is already in a terminal state: {status}")
else:
    cancel_tapis_job(t, job_id)
```
