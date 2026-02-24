def analyze_tacc_job_history(t, jobUuid, mode="summary"):
    """
    Wrapper for process_tacc_job_history with different preset modes.
    
    Modes:
        - "summary": shows key stages and durations
        - "full": prints everything (like printAllAll=True)
        - "data": returns structured data only, no prints
    """
    # Silvia Mazzoni, 2025
    if mode == "summary":
        process_tacc_job_history(
            t, jobUuid,
            printSteps=True,
            printDurations=True,
            printInput=True,
            returnData=False
        )
    elif mode == "full":
        process_tacc_job_history(
            t, jobUuid,
            printAllAll=True,
            returnData=False
        )
    elif mode == "data":
        return process_tacc_job_history(
            t, jobUuid,
            printSteps=False,
            printDurations=False,
            printInput=False,
            returnData=True
        )
    else:
        print(f"Unknown mode: {mode}. Use 'summary', 'full', or 'data'.")
