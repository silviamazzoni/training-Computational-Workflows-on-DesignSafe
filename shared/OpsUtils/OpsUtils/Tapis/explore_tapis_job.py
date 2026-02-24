def explore_tapis_job(t, jobUuid):
    """
    Explore a Tapis job: print name/status, show history, and list outputs.
    Works in plain Python/terminal and (optionally) enhances UX in Jupyter
    by showing a dropdown to select downloadable files if ipywidgets is available.

    Behavior
    --------
    - Prints: job UUID, job name, current status.
    - Prints: a formatted **job history** using OpsUtils.process_tacc_job_history.
    - Prints: job outputs (files and directories). If running in a notebook with
      ipywidgets installed, shows a dropdown selector and a download button hook.
    - Returns a structured dict with the job metadata, status, and output listings.

    Parameters
    ----------
    t : tapipy.tapis.Tapis
        An authenticated Tapis client.
    jobUuid : str
        The UUID of the job to explore.

    Returns
    -------
    dict
        {
          "jobUuid": <str>,
          "name": <str or None>,
          "status": <str or None>,
          "outputs": [
              {"path": <str>, "type": <"file"|"dir"|"archive"|...>}
          ],
          "inputDirectoryOutputs": [
              {"path": <str>, "type": <"file"|"dir"|"archive"|...>}
          ]
        }

    Notes
    -----
    - If ipywidgets is unavailable, the function still prints outputs and returns data.
    - If OpsUtils.process_tacc_job_history is missing, the function prints a note and continues.

    Example
    -------
    info = explore_tapis_job(t, "1b2c3d4e-...-...-...")
    print(len(info["outputs"]))

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
    from datetime import datetime
    print(f"--- Exploring job UUID: {jobUuid} ---")

    # Try to import helpers (optional UI in notebooks)
    have_widgets = False
    outputs_dropdown = None
    download_button = None
    display_fn = None
    try:
        from ipywidgets import Dropdown, Button
        from IPython.display import display as _display
        outputs_dropdown = Dropdown(description="Outputs:", options=[])
        download_button = Button(description="Download")
        display_fn = _display
        have_widgets = True
    except Exception:
        # Not a notebook environment or ipywidgets missing — proceed without UI
        pass

    # Fetch job metadata and status (robust to API hiccups)
    name = None
    status = None
    try:
        job_meta = t.jobs.getJob(jobUuid=jobUuid)
        name = getattr(job_meta, "name", None)
    except Exception as e:
        print(f" [warn] Could not fetch job metadata: {e}")

    try:
        job_status = t.jobs.getJobStatus(jobUuid=jobUuid)
        status = getattr(job_status, "status", None)
    except Exception as e:
        print(f" [warn] Could not fetch job status: {e}")

    print("Job name:", name if name is not None else "(unknown)")
    print("Status:", status if status is not None else "(unknown)")

    # Job history
    print("\n***************************************")
    print("********    JOB HISTORY     ***********")
    print("***************************************")
    try:
        from OpsUtils import OpsUtils
        # Your original helper (assumed to print a readable history)
        OpsUtils.process_tacc_job_history(t, jobUuid)
    except Exception as e:
        print(f" [warn] Could not render job history (OpsUtils?): {e}")
    print("***************************************")
    print("********   END JOB HISTORY   **********")
    print("***************************************\n")

    # Outputs (root)
    outputs = []
    try:
        listing = t.jobs.getJobOutputList(jobUuid=jobUuid, outputPath=".")
        outputs = [{"path": getattr(o, "path", ""), "type": getattr(o, "type", "")} for o in (listing or [])]
    except Exception as e:
        print(f" [warn] Could not list outputs: {e}")
        listing = []

    if not listing:
        print(" No output files found.")
        if have_widgets:
            outputs_dropdown.options = []
    else:
        print("Outputs:")
        for out in listing:
            print(f" - {getattr(out, 'path', '')} ({getattr(out, 'type', '')})")

    # Look for inputDirectory and list it if present
    found_input_dir = any(
        (getattr(o, "type", "") != "file") and ("inputDirectory" in getattr(o, "path", ""))
        for o in (listing or [])
    )
    input_dir_outputs = []
    if found_input_dir:
        print("-- looking in inputDirectory --")
        try:
            sub_listing = t.jobs.getJobOutputList(jobUuid=jobUuid, outputPath="./inputDirectory")
            input_dir_outputs = [{"path": getattr(o, "path", ""), "type": getattr(o, "type", "")} for o in (sub_listing or [])]
            if not sub_listing:
                print(" No output files found in inputDirectory.")
            else:
                print("inputDirectory-Outputs:")
                for out in sub_listing:
                    print(f"   - {getattr(out, 'path', '')} ({getattr(out, 'type', '')})")
        except Exception as e:
            print(f" [warn] Could not list inputDirectory outputs: {e}")

    # Populate dropdown if running in a notebook with ipywidgets
    if have_widgets:
        file_options = []
        for rec in outputs + input_dir_outputs:
            if rec.get("type") == "file":
                p = rec.get("path", "")
                file_options.append((p, p))
        if file_options:
            outputs_dropdown.options = file_options
            print("\n(Notebook helpers) Choose a file to download:")
            display_fn(outputs_dropdown, download_button)
        else:
            outputs_dropdown.options = []

    # Return structured info for programmatic use
    return {
        "jobUuid": jobUuid,
        "name": name,
        "status": status,
        "outputs": outputs,
        "inputDirectoryOutputs": input_dir_outputs,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
