def cancel_tapis_job(tapis_client, job_uuid):
    """
    Attempts to cancel a Tapis job by UUID, with basic error handling and status confirmation.

    Parameters:
    - tapis_client: Authenticated tapipy.Tapis client
    - job_uuid (str): UUID of the job to cancel

    Returns:
    - status (str): Final reported job status (e.g., CANCELLED, FINISHED, FAILED)
    """
    try:
        # Attempt to cancel the job
        tapis_client.jobs.cancelJob(jobId=job_uuid)
        print(f"Job {job_uuid} cancellation requested...")

        # Confirm the updated job status
        job_status = tapis_client.jobs.getJob(jobId=job_uuid).status
        print(f"✅ Current job status: {job_status}")

        return job_status

    except Exception as e:
        # Handle known issues
        error_message = str(e)

        if "Job not found" in error_message:
            print(f"## Error ##: Job {job_uuid} not found. Check the UUID.")
        elif "Invalid job state" in error_message:
            print(f"** Warning **: Job {job_uuid} may already be completed or cancelled.")
        else:
            print(f"Unexpected error cancelling job {job_uuid}: {error_message}")

        return None
