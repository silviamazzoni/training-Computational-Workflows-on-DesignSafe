def get_tapis_job_status(t, jobUuid, print_all=True, return_values=False):
    """
    Retrieve and optionally display the status of a Tapis job.

    Summary
    -------
    Queries the Tapis Jobs service for the current status of the job identified by
    `jobUuid`. By default, prints the status in an expandable Jupyter widget with
    details including the job's UUID, current state, and any associated message.

    Parameters
    ----------
    t : tapipy.tapis.Tapis
        Authenticated Tapis client instance.
    jobUuid : str
        The UUID of the Tapis job to query.
    print_all : bool, default True
        If True, display status and details in a Jupyter accordion widget.
        If False, suppress printing.
    return_values : bool, default False
        If True, return the `JobStatus` object from Tapis.
        If False, return None.

    Returns
    -------
    tapipy.tapis.TapisResult or None
        - If `return_values` is True, returns the Tapis job status object.
        - Otherwise, returns None.

    Notes
    -----
    When `print_all` is True, the output includes:
    * The job UUID
    * The raw job status object
    * An optional `message` field from the Tapis status
    * Error message summary (via `OpsUtils.get_tapis_job_history_data`)

    Example
    -------
    >>> get_tapis_job_status(t, "1234-uuid-5678")
    ++++++++++++++++++++++++++++++
    ++++++ Job Status ++++++
    ++++++++++++++++++++++++++++++
    jobUuid: 1234-uuid-5678
    Job Status: TapisResult(...)
    ++++++++++++++++++++++++++++++

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
    from OpsUtils import OpsUtils
    JobStatus = t.jobs.getJobStatus(jobUuid=jobUuid)

    if print_all:
        import ipywidgets as widgets
        from IPython.display import display
        this_out = widgets.Output()
        this_accordion = widgets.Accordion(children=[this_out])
        this_accordion.set_title(0, f'Job STATUS   ({jobUuid})')
        this_accordion.selected_index = 0
        display(this_accordion)

        with this_out:
            print('+' * 30)
            print(f'++++++ Job Status ++++++')
            print('+' * 30)
            print(f'jobUuid: {jobUuid}')
            print(f'Job Status: {JobStatus}')
            print('+' * 30)

            if hasattr(JobStatus, "message"):
                print('message:', JobStatus.message)
                print('+' * 30)

            OpsUtils.get_tapis_job_history_data(
                t, jobUuid,
                print_out=False,
                return_data=False,
                get_job_error_message=True
            )

    if return_values:
        return JobStatus
    else:
        return
