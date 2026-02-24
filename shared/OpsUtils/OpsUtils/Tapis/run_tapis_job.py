def run_tapis_job(
    t,
    tapisInput,
    askConfirmJob: bool = True,
    monitor_job: bool = True,
    askConfirmMonitorRT: bool = True,
    get_job_history: bool = False,
    get_job_metadata: bool = False,
    get_job_filedata: bool = False,
    job_description = {}
):
    """
    Run a complete Tapis job workflow in one call: build (or accept) a job description,
    submit, and optionally monitor + collect results (status/metadata/history/file data).

    Workflow
    --------
    1) If `job_description` is provided (non-empty dict), use it as-is; otherwise,
       build one from `tapisInput` via `OpsUtils.get_tapis_job_description`.
    2) Submit the job via `OpsUtils.submit_tapis_job` (with optional confirmation).
    3) If `monitor_job=True`, call `OpsUtils.monitor_tapis_job` and then:
       - Always fetch basic status via `OpsUtils.get_tapis_job_status`.
       - If `get_job_metadata=True`, fetch detailed metadata via
         `OpsUtils.get_tapis_job_metadata` (this overwrites the basic status dict).
       - If `get_job_history=True`, fetch history via `OpsUtils.get_tapis_job_history_data`.
       - If `get_job_filedata=True`, fetch output file listings/data via
         `OpsUtils.get_tapis_job_all_files`.

    Parameters
    ----------
    t : tapipy.tapis.Tapis
        Authenticated Tapis client.
    tapisInput : dict
        Fields used to construct the job description (e.g., name, appId, inputs) when
        `job_description` is not provided.
    askConfirmJob : bool, default True
        Ask for confirmation before submitting.
    monitor_job : bool, default True
        Monitor the job in real time after submission. Required for the code paths that
        fetch status/metadata/history/file data in this function.
    askConfirmMonitorRT : bool, default True
        Ask for confirmation before starting real-time monitoring.
    get_job_history : bool, default False
        If True and `monitor_job=True`, include job history in the return object.
    get_job_metadata : bool, default False
        If True and `monitor_job=True`, include detailed job metadata in the return object
        (overwrites the basic status dict).
    get_job_filedata : bool, default False
        If True and `monitor_job=True`, include job output file listings/data.
    job_description : dict, default {}
        Optional pre-built Tapis job description. If provided (non-empty), it takes
        precedence over building from `tapisInput`.

    Returns
    -------
    dict
        A dictionary seeded from `OpsUtils.submit_tapis_job(...)`, augmented with:
          - 'job_description' : dict
          - 'JobHistory'      : dict or {}
          - 'JobMetadata'     : dict or {}
          - 'JobFiledata'     : dict or {}
          - 'runJobStatus'    : 'Finished' | 'Incomplete' | other
        If `OpsUtils.get_tapis_job_description(...)` fails, returns:
          {'runJobStatus': 'Incomplete'}

    Notes
    -----
    - Status/metadata/history/file data are gathered only when `monitor_job=True`.
    - If `OpsUtils.submit_tapis_job` yields a status other than 'Finished', the function
      returns that object unchanged (except the early 'Incomplete' short-circuit).

    Example
    -------
    result = run_tapis_job(
        t, tapisInput,
        monitor_job=True,
        get_job_history=True,
        get_job_metadata=True
    )
    print("Job UUID:", result.get("jobUuid"))
    print("Status:",   result.get("JobMetadata", {}).get("status"))

    Author
    ------
    Silvia Mazzoni, DesignSafe (silviamazzoni@yahoo.com)

    Date
    ----
    2025-08-16

    Version
    -------
    1.1
    """

    from OpsUtils import OpsUtils
    import ipywidgets as widgets
    from IPython.display import display, clear_output
    job_out = widgets.Output()
    job_accordion = widgets.Accordion(children=[job_out])
    job_accordion.selected_index = 0
    display(job_accordion)
    job_accordion.set_title(0, f'Job Run ....')

    with job_out:
        desc_out = widgets.Output()
        desc_accordion = widgets.Accordion(children=[desc_out])
        # desc_accordion.selected_index = 0
        desc_accordion.set_title(0, f'Job Input')
        
        display(desc_accordion)
        with desc_out:
            if not job_description:
                job_description = OpsUtils.get_tapis_job_description(t, tapisInput)
            print('########################################')
            print('##  job_description (tapis-app INPUT) ##')
            OpsUtils.display_tapis_results(job_description);
        
        if job_description == -1:
            return {"runJobStatus": "Incomplete"}
    
        submit_out = widgets.Output()
        submit_accordion = widgets.Accordion(children=[submit_out])
        # submit_accordion.selected_index = 0
        
        submit_accordion.set_title(0, f'Submit Returned Data')

        with submit_out:
            returnDict = OpsUtils.submit_tapis_job(t, job_description, askConfirmJob)

        
            OpsUtils.display_tapis_results(returnDict)
        
        display(submit_accordion)
        
        if returnDict.get("runJobStatus") == "Submitted":

            monitor_out = widgets.Output()
            monitor_accordion = widgets.Accordion(children=[monitor_out])
            monitor_accordion.selected_index = 0
            monitor_accordion.set_title(0, f'Monitor Job')
            display(monitor_accordion)
            with monitor_out:
            
                print("job_start_time:", returnDict.get("job_start_time"))
            jobUuid = returnDict.get("jobUuid")
            job_accordion.set_title(0, f'Job Run:  {jobUuid} ...')
    
            JobHistory = {}
            JobMetadata = {}
            JobFiledata = {}
            JobStatusData = {}
    
            if monitor_job and jobUuid:
                with monitor_out:
                    OpsUtils.monitor_tapis_job(t, jobUuid, returnDict.get("job_start_time"), askConfirmMonitorRT)
    
                # Always fetch basic status after monitoring
                JobStatusData = OpsUtils.get_tapis_job_status(t, jobUuid, tapisInput,return_values=True)
                job_accordion.set_title(0, f'Job :  {jobUuid} {JobStatusData.status} {JobStatusData.condition}')
    
                # Optional enrichments
                if get_job_metadata:
                    JobMetadata = OpsUtils.get_tapis_job_metadata(t, jobUuid, tapisInput)
                if get_job_history:
                    JobHistory = OpsUtils.get_tapis_job_history_data(t, jobUuid)
                if get_job_filedata:
                    JobFiledata = OpsUtils.get_tapis_job_all_files(t, jobUuid)
    
            # Augment return object
            returnDict["job_description"] = job_description
            returnDict["JobHistory"] = JobHistory
            returnDict["JobMetadata"] = JobMetadata
            returnDict["JobFiledata"] = JobFiledata
            returnDict["JobStatusData"] = JobStatusData
            returnDict["runJobStatus"] = "Finished"

    job_accordion.set_title(0, f'Job Run:  {jobUuid} done!')

    return returnDict
