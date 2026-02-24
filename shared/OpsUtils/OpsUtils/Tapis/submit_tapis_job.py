def submit_tapis_job(t, job_description, askConfirmJob: bool = True):
    """
    Submit a job to the Tapis Jobs service with optional interactive confirmation.

    Summary
    -------
    Uses an authenticated Tapis client to submit a job defined by `job_description`.
    By default, asks the user to confirm before launching to avoid accidental
    submissions. On success, prints the assigned job UUID and records a local
    submission timestamp.

    Parameters
    ----------
    t : tapipy.tapis.Tapis
        Authenticated Tapis client instance.
    job_description : dict
        Dictionary describing the Tapis job (typically from a helper like
        `get_tapis_job_description()`).
    askConfirmJob : bool, default True
        If True, prompt for confirmation before submitting. If False, submit
        immediately.

    Returns
    -------
    dict
        On successful submission:
            {
              'jobUuid': <str>,          # UUID of the submitted job
              'submitted_job': <object>, # full Tapis job object
              'job_start_time': <float>, # local epoch time at submission
              'runJobStatus': 'Finished'
            }
        If submission is cancelled (or not confirmed):
            {
              'runJobStatus': 'Incomplete'
            }

    Prints
    ------
    Messages indicating whether submission was confirmed, cancelled, or completed,
    along with the assigned Tapis job UUID.

    Example
    -------
    result = submit_tapis_job(t, job_description)
    if result.get('runJobStatus') == 'Finished':
        print('Job UUID:', result['jobUuid'])

    Author
    ------
    Silvia Mazzoni, DesignSafe (silviamazzoni@yahoo.com)

    Date
    ----
    2025-08-14

    Version
    -------
    1.0
    """
    # Silvia Mazzoni, 2025
    import time

    if askConfirmJob:
        try:
            ConfirmJob = input(
                'Are you sure you want to submit the job? '
                '(press n to cancel, any key to confirm): '
            )
        except EOFError:
            # Non-interactive environment: treat as cancel for safety
            ConfirmJob = 'n'
    else:
        ConfirmJob = 'y'

    # GO!
    if len(ConfirmJob) > 0 and ConfirmJob.lower()[0] == 'n':
        print('okey, bye!')
        return {'runJobStatus': 'Incomplete'}
    else:
        # Submit job
        print("Submitting Job")
        submitted_job = t.jobs.submitJob(**job_description)
        jobUuid = submitted_job.uuid
        print(f"Job submitted! ID: {jobUuid}")
        job_start_time = time.time()

        return {
            'jobUuid': jobUuid,
            'submitted_job': submitted_job,
            'job_start_time': job_start_time,
            'runJobStatus': 'Submitted',
        }
