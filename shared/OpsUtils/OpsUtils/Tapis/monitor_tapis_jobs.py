def monitor_tapis_jobs(t, jobUuid, job_start_time, askConfirmMonitorRT=True):
    """
    Monitors the status of a Tapis job in real-time, printing structured updates until completion.

    This function repeatedly polls the Tapis job service for the current job status,
    printing elapsed time and status transitions. It gradually increases the polling
    interval to avoid overwhelming the server. Monitoring stops automatically if the
    job finishes (status in ["FINISHED", "FAILED", "STOPPED"]),
    after exceeding a maximum allowed monitoring time (default 1 hour),
    or after too many consecutive failed API calls.

    Parameters
    ----------
    t : object
        An authenticated Tapis client instance (e.g., from `tapis3`).
    jobUuid : str
        UUID of the job to monitor.
    job_start_time : float
        Time when the job was submitted (epoch seconds, e.g. from `time.time()`).
    askConfirmMonitorRT : bool, optional
        If True (default), prompts the user to confirm starting monitoring.
        If False, begins monitoring immediately without asking.

    Returns
    -------
    None
        This function does not return anything. It prints progress and status
        updates to the console in real-time.

    Prints
    ------
    Structured updates such as:
        Elapsed job time: <seconds>    Current Status: <status>    (previous <status> took <seconds> sec)
    and a final summary with total monitoring time.

    Example
    -------
    >>> monitor_tapis_job(t, jobUuid, time.time())
    >>> monitor_tapis_job(t, jobUuid, time.time(), askConfirmMonitorRT=False)
    """
    # Silvia Mazzoni, 2025
    # MONITOR in REALtime
    import time
    # Ask for confirmation
    # askConfirmMonitorRT = True; # make false if you definitly want to submit without user confirmation.
    if askConfirmMonitorRT:
        ConfirmMonitorRT = input(f'Do you want to monitor the job in real-time? (press n to cancel, any key to confirm): ')
    else:
        ConfirmMonitorRT = 'yes' ;
    if len(ConfirmMonitorRT)>0 and ConfirmMonitorRT.lower()[0] == 'n':
        print('okey, bye!')
    else:
        tlapseStart = 1
        elapsed_time_max = 60*60
        icountMax = 100
        Dlapse = 5
        nfailMax = 10
        print("\nReal-Time Job-Status Updates...")
        print("--------------------") 
        start_time = job_start_time
        status = t.jobs.getJobStatus(jobUuid=jobUuid).status
        previous = ""
        icount = 0
        tlapse=tlapseStart
        # print(f'tlapse = {tlapse} sec')
        nfail = 0
        now_time = job_start_time
        while True:
            try:
                status = t.jobs.getJobStatus(jobUuid=jobUuid).status
            except:
                nfail +=1
                if nfail>=nfailMax:
                    print(f'Unable to reach tapis after {nfail} tries')
            # if status in ["FINISHED","FAILED","STOPPED"]:
            #     break
            icount+=1
            if icount==icountMax:
                tlapse = tlapse*Dlapse
                icount = 0
                # print(f'new tlapse = {tlapse} sec')
            time.sleep(tlapse)
            if status == previous: continue
            previousprevious = previous
            previous = status
            prev_time = now_time
            now_time = time.time()
            elapsed_time = round(now_time - start_time,2)
            elapsed_prev_time = round(now_time - prev_time,2)
            
            if elapsed_time>elapsed_time_max:
                print(f'Monitoring time has exceeded {elapsed_time_max} sec ({round(elapsed_time_max/60/60)}-hour)')
                break
            prevTime = ''
            if previousprevious!='':
                prevTime = f"\t\t({previousprevious} took {elapsed_prev_time} sec)"
            print(f"\t Elapsed job time: {elapsed_time} sec\t Current Status: {status}{prevTime}")
            if status in ["FINISHED","FAILED","STOPPED"]:
                break        
            
        end_time = time.time()
        elapsed_time = round(end_time - start_time,2)
        print(f"\t  Status: {status}\t Elapsed job time: {elapsed_time} sec\n--------------------")
        elapsed_time_job = round(end_time - start_time,2)
        print(f"Elapsed time since Job was submitted: {elapsed_time_job} sec\n--------------------")