def get_tapis_job_history_data(
    t,
    jobUuid: str,
    print_out: bool = True,
    return_data: bool = False,
    get_job_error_message: bool = False,
):
    """
    Retrieve and summarize a TACC/Tapis job's history, including step durations,
    data-transfer metrics, and any job error messages. Optionally prints a
    readable summary (Jupyter-friendly if ipywidgets is available) and/or
    returns structured data for further analysis.

    What it does
    ------------
    - Calls `t.jobs.getJobHistory(jobUuid=...)`.
    - Computes time spent in each job status (e.g., QUEUED, RUNNING).
    - Extracts transfer metrics for input/archive staging events.
    - Collects JOB_ERROR_MESSAGE entries (if present).
    - Prints accordion-style sections in Jupyter (if ipywidgets is available),
      otherwise prints plain text sections.
    - Optionally returns structured dictionaries.

    Parameters
    ----------
    t : tapipy.tapis.Tapis
        Authenticated Tapis client.
    jobUuid : str
        Job UUID to inspect.
    print_out : bool, default True
        If True, print summaries (accordion in Jupyter, plain text otherwise).
    return_data : bool, default False
        If True, return structured data dictionaries (see Returns).
    get_job_error_message : bool, default False
        If True, ensure error messages section prints (if any are found).

    Returns
    -------
    dict | int | None
        - When `return_data=True`, returns:
            {
              "StepsMetricsDict": { "created": {...}, "duration": {..., "TOTAL": seconds} },
              "DataTransfersDict": { <event>: {metrics...}, ... },
              "JobHistory": <list of history entries as returned by Tapis>,
              "JobErrorList": [ {event, created, eventDetail, jobStatus, message}, ... ]
            }
        - If an API error occurs (fetching history), returns `-1`.
        - Otherwise returns `None`.

    Example
    -------
    # Print to screen and get data back:
    info = get_tapis_job_history_data(t, jobUuid, print_out=True, return_data=True)
    print(info["StepsMetricsDict"]["duration"].get("RUNNING", 0))

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
    from datetime import datetime, timezone
    from OpsUtils import OpsUtils

    # --- Helpers -------------------------------------------------------------
    def _parse_tacc_time(ts: str) -> float:
        """
        Parse Tapis/TACC ISO timestamps to a Unix epoch (float seconds).
        Accepts microseconds or no microseconds; 'Z' treated as UTC.
        """
        if not ts:
            return 0.0
        s = ts.strip().replace("Z", "+00:00")
        try:
            # Try with microseconds first
            dt = datetime.fromisoformat(s)
        except ValueError:
            # Fallbacks if some variants sneak in; best-effort
            try:
                # Remove fractional seconds if present and retry
                if "." in s:
                    s2 = s.split(".", 1)[0] + "+00:00"
                    dt = datetime.fromisoformat(s2)
                else:
                    raise
            except Exception:
                # Return 0.0 if we cannot parse
                return 0.0
        # Make sure it's timezone-aware UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()

    def _get_job_history(t, jobUuid):
        try:
            return t.jobs.getJobHistory(jobUuid=jobUuid)
        except Exception as e:
            print(e)
            return -1

    # --- Fetch history -------------------------------------------------------
    JobHistory = _get_job_history(t, jobUuid)
    if JobHistory == -1:
        return -1

    # --- Print toggles -------------------------------------------------------
    printStepDurations = bool(print_out)
    printInput = bool(print_out)
    printAllSteps = bool(print_out)
    printLastStep = bool(print_out)
    printJobErrorMessage = bool(print_out) or bool(get_job_error_message)

    # --- Accumulators --------------------------------------------------------
    STATdur = [
        "\n++++++++++++++++++++++++++++++++++++++++++++++++++",
        "+ STEP DURATION +",
        "++++++++++++++++++++++++++++++++++++++++++++++++++",
    ]
    INPUTdur = []
    AllStepList = [
        "\n++++++++++++++++++++++++++++++++++++++++++++++++++",
        "+ STEP DETAILS +",
        "++++++++++++++++++++++++++++++++++++++++++++++++++",
    ]
    LastStepList = [
        "\n++++++++++++++++++++++++++++++++++++++++++++++++++",
        "+ LAST-STEP DETAILS +",
        "++++++++++++++++++++++++++++++++++++++++++++++++++",
    ]
    totalT = 0.0
    stepDict = {"created": {}, "duration": {}}
    transfersDict = {}
    JobErrorList = []

    # --- Iterate through history --------------------------------------------
    NHistoryLines = len(JobHistory)
    prev_created_ts = 0.0
    prev_status = None
    prev_created_str = None

    for idx, thisHistoryLine in enumerate(JobHistory):
        AllStepList.append(f"Step {idx+1} of {NHistoryLines}")
        AllStepList.append("-" * 40)
        if idx == NHistoryLines - 1:
            LastStepList.append(f"Step {idx+1} of {NHistoryLines}")
            LastStepList.append("-" * 40)

        Hdict = thisHistoryLine.__dict__
        flat_hist = OpsUtils.flatten_dict(Hdict)

        event = flat_hist.get("event", "")
        created = flat_hist.get("created", "")
        created_ts = _parse_tacc_time(created)
        eventDetail = flat_hist.get("eventDetail", "")

        # Track status durations
        if event == "JOB_NEW_STATUS":
            new_status = flat_hist.get("description.newJobStatus", "")
            old_status = flat_hist.get("description.oldJobStatus", "")

            if prev_created_ts > 0 and prev_status:
                dTime = round(created_ts - prev_created_ts, 1)
                pad = " " * max(1, 20 - len(prev_status))
                STATdur.append(f"  {prev_status}:{pad} {dTime} sec   \t created: {prev_created_str}")
                stepDict["created"][prev_status] = prev_created_str
                stepDict["duration"][prev_status] = dTime
                totalT += dTime

            # advance previous pointers
            prev_created_ts = created_ts
            prev_created_str = created
            prev_status = new_status

        elif event in ("JOB_INPUT_TRANSACTION_ID", "JOB_ARCHIVE_TRANSACTION_ID"):
            # Label section by event type
            header_label = "INPUT TRANSFER" if event == "JOB_INPUT_TRANSACTION_ID" else "ARCHIVE TRANSFER"
            INPUTdur.append(f"\n----------------------\n {header_label}\n----------------------")
            INPUTdur.append("  ------------- Transfer Summary -------------")
            transfersDict[event] = {}

            # Summary numbers (if available)
            for k in ("estimatedTotalBytes", "totalBytesTransferred", "completeTransfers", "totalTransfers"):
                v = flat_hist.get(f"transferSummary.{k}")
                pad = " " * max(1, 25 - len(k))
                INPUTdur.append(f"  {k}:{pad} {v}")
                transfersDict[event][k] = v

            # Durations
            INPUTdur.append("  ------------- Transfer Duration -------------")
            created_t = _parse_tacc_time(flat_hist.get("transferSummary.created", ""))
            start_t = _parse_tacc_time(flat_hist.get("transferSummary.startTime", ""))
            end_t = _parse_tacc_time(flat_hist.get("transferSummary.endTime", ""))

            d1 = round(start_t - created_t, 1) if (start_t and created_t) else None
            d2 = round(end_t - start_t, 1) if (end_t and start_t) else None
            d3 = round(end_t - created_t, 1) if (end_t and created_t) else None

            INPUTdur.append(f"  Create-to-TransferStart Duration: {d1} sec")
            INPUTdur.append(f"  TransferStart-to-TransferEnd Duration: {d2} sec")
            INPUTdur.append(f"  Create-to-TransferEnd Duration: {d3} sec")

            transfersDict[event]["Create-to-TransferStart Duration"] = d1
            transfersDict[event]["TransferStart-to-TransferEnd Duration"] = d2
            transfersDict[event]["Create-to-TransferEnd Duration"] = d3

        elif event == "JOB_ERROR_MESSAGE":
            JobErrorDict = {
                "event": event,
                "created": flat_hist.get("created"),
                "eventDetail": flat_hist.get("eventDetail"),
                "jobStatus": flat_hist.get("description.jobStatus"),
                "message": flat_hist.get("description.message"),
            }
            JobErrorList.append(JobErrorDict)

        # Append all flattened fields (nice for inspection)
        for k, n in flat_hist.items():
            if n is None or str(n) == "":
                continue
            line = f"{k:<35} : {n}"
            AllStepList.append(line)
            if idx == NHistoryLines - 1:
                LastStepList.append(line)

        AllStepList.append("-" * 40)
        if idx == NHistoryLines - 1:
            LastStepList.append("-" * 40)

    # Finalize totals (note: if job is still RUNNING/QUEUED the last segment is open)
    STATdur.append(f"  Total Duration: {round(totalT, 1)} sec")
    stepDict["duration"]["TOTAL"] = round(totalT, 1)

    # --- Printing (Jupyter accordion if available) ---------------------------
    def _print_sections_plain():
        if printJobErrorMessage and JobErrorList:
            print("\n++++++++++++++++++++++++++++")
            print("++++++ JOB-ERROR MESSAGE ++++++")
            print("++++++++++++++++++++++++++++")
            for d in JobErrorList:
                for k, v in d.items():
                    print(f"{k}:\t{v}")
                print("------")
        if printStepDurations:
            for line in STATdur:
                print(line)
        if printInput and INPUTdur:
            print("\n".join(INPUTdur))
        if printAllSteps:
            print("\n".join(AllStepList))
        if printLastStep:
            print("\n".join(LastStepList))

    def _print_sections_widgets():
        import ipywidgets as widgets
        from IPython.display import display

        history_out = widgets.Output()
        acc = widgets.Accordion(children=[history_out])
        acc.set_title(0, f"Job History Data   ({jobUuid})")
        acc.selected_index = 0
        display(acc)
        with history_out:
            print("\n++++++++++++++++++++++++++++")
            print("++++++ JOB-HISTORY DATA ++++++")
            print("++++++++++++++++++++++++++++++")
            print(f"++++++ jobUuid: {jobUuid}")
            print("+++++++++++++++++++++++++")

        if printJobErrorMessage and JobErrorList:
            out = widgets.Output()
            acc2 = widgets.Accordion(children=[out])
            acc2.set_title(0, "Job ERROR MESSAGE")
            acc2.selected_index = 0
            with history_out:
                display(acc2)
            with out:
                for d in JobErrorList:
                    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++")
                    print("+ JOB_ERROR_MESSAGE +")
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++")
                    for k, v in d.items():
                        print(f"{k}:\t{v}")
                    print("------")

        if printStepDurations:
            out = widgets.Output()
            acc2 = widgets.Accordion(children=[out])
            acc2.set_title(0, "Steps Duration")
            with history_out:
                display(acc2)
            with out:
                for line in STATdur:
                    print(line)
                print("++++++++++++++++++++++++++++++++++++++++++++++++++")

        if printInput and INPUTdur:
            out = widgets.Output()
            acc2 = widgets.Accordion(children=[out])
            acc2.set_title(0, "Job-Stagings Info")
            with history_out:
                display(acc2)
            with out:
                for line in INPUTdur:
                    print(line)
                print("++++++++++++++++++++++++++++++++++++++++++++++++++")

        if printAllSteps:
            out = widgets.Output()
            acc2 = widgets.Accordion(children=[out])
            acc2.set_title(0, "ALL Steps Info")
            with history_out:
                display(acc2)
            with out:
                for line in AllStepList:
                    print(line)
                print("++++++++++++++++++++++++++++++++++++++++++++++++++")

        if printLastStep:
            out = widgets.Output()
            acc2 = widgets.Accordion(children=[out])
            acc2.set_title(0, "Last Step Info")
            with history_out:
                display(acc2)
            with out:
                for line in LastStepList:
                    print(line)
                print("++++++++++++++++++++++++++++++++++++++++++++++++++")

    if print_out:
        try:
            _print_sections_widgets()
        except Exception:
            _print_sections_plain()

    # --- Return data ---------------------------------------------------------
    if return_data:
        return {
            "StepsMetricsDict": stepDict,
            "DataTransfersDict": transfersDict,
            "JobHistory": JobHistory,
            "JobErrorList": JobErrorList,
        }
    else:
        return
