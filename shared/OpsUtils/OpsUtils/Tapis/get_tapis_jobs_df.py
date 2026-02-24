def get_tapis_jobs_df(t, displayIt=False, NmaxJobs=500):
    """
    Retrieve a list of jobs from Tapis and organize them into a Pandas DataFrame.

    This function fetches up to NmaxJobs from the user's Tapis account, converts the 
    results into a structured DataFrame, adds a convenient index column, and moves key 
    metadata columns (like name, uuid, status) to the front for easier exploration.

    It can also optionally display the DataFrame (entire or just the head) right in 
    the notebook for quick inspection.

    Parameters
    ----------
    t : Tapis
        An authenticated Tapis client (from connect_tapis()).

    displayIt : bool or str, default=False
        If 'head' or 'displayHead', displays only the first few rows.
        If True or 'displayAll', displays the entire DataFrame.
        If False, no display output (just returns the DataFrame).

    NmaxJobs : int, default=500
        Maximum number of jobs to retrieve from Tapis.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing metadata for the fetched jobs.

    Example
    -------
    df = get_tapis_jobs_df(t, displayIt='head', NmaxJobs=1000)
    """
    # Silvia Mazzoni, 2025

    from datetime import datetime, timezone
    import pandas as pd

    # Get jobs from Tapis
    jobslist = t.jobs.getJobList(limit=NmaxJobs)
    
    # Convert TapisResult objects to dictionaries
    jobsdicts = [job.__dict__ for job in jobslist]
    
    # Build DataFrame
    df = pd.DataFrame(jobsdicts)
    
    # Add index column for convenience
    df["index_column"] = df.index
    
    # add formatted data
    for thisK in ['created','remoteStarted', 'ended','lastUpdated']:
        df[f'{thisK}_dt'] = pd.to_datetime(df[thisK], utc=True)
        df[f'{thisK}_unix'] = df[f'{thisK}_dt'].astype('int64') // 10**9
        df[f'{thisK}_date'] = df[f'{thisK}_unix'].apply(
                    lambda x: datetime.fromtimestamp(x, tz=timezone.utc).date()
                )

    
    # Reorder columns: put key ones first if they exist
    startCols = ['index_column', 'name', 'uuid', 'status', 'appId', 'appVersion']
    existingStartCols = [col for col in startCols if col in df.columns]
    remainingCols = [col for col in df.columns if col not in existingStartCols]
    columns = existingStartCols + remainingCols
    df = df[columns]
    
    # Optional display logic
    if displayIt != False:
        print(f'Found {len(df)} jobs')
        
        if displayIt in [True] or displayIt.lower() in ['display','displayall','all']:
            display(df)
        elif displayIt.lower() in ['head', 'displayHead']:
            display(df.head())
    
    return df



    