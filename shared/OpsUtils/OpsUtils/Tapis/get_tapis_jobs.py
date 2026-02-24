def get_tapis_jobs(t, SelectCriteria, displayIt=False, NmaxJobs=500):
    """
    Filter Tapis jobs based on flexible selection criteria, including time ranges, 
    specific dates, status, appId, or any other metadata field.

    This function pulls a DataFrame of your jobs via get_tapis_jobs_df, then applies
    the filters specified in SelectCriteria to return only the matching jobs.

    Supports:
    ----------
    - Date range filtering (for 'created', 'remoteStarted', 'ended', 'lastUpdated')
      by providing a list like ['YYYY-MM-DD', 'YYYY-MM-DD'].
    - Single date filtering by providing a single 'YYYY-MM-DD' string.
    - Filtering on any other field using exact match or a list of values.

    Parameters
    ----------
    t : Tapis
        An authenticated Tapis client (from connect_tapis()).

    SelectCriteria : dict
        Dictionary where keys are field names and values are:
        - A single value for exact matching, e.g. {'status': 'FINISHED'}
        - A list of values for multiple match, e.g. {'status': ['FINISHED', 'FAILED']}
        - For time fields, a list of two dates for range filtering, 
          or a single date string for exact date matching.

    displayIt : bool, str, default=False
        If True, prints and displays all filtered UUIDs and metadata.
        If 'head', only prints the top of the filtered DataFrame.

    NmaxJobs : int, default=500
        Max number of jobs to retrieve from Tapis before filtering.

    Returns
    -------
    (list, DataFrame)
        A tuple containing:
        - List of UUIDs of jobs that matched the filters.
        - The filtered Pandas DataFrame itself.

    Example
    -------
    SelectCriteria = {
        'created': ['2025-06-01', '2025-06-30'],
        'status': ['FINISHED', 'FAILED'],
        'appId': 'opensees-mp'
    }
    uuids, df = get_tapis_job(t, SelectCriteria, displayIt=True)
    """
    # Silvia Mazzoni, 2025
    from datetime import datetime, timezone
    import re
    from OpsUtils import OpsUtils

    filtered_df = OpsUtils.get_tapis_jobs_df(t, displayIt=False, NmaxJobs=500)

    for key, values in SelectCriteria.items():
        if key in ['created', 'remoteStarted', 'ended','lastUpdated']:
            filtered_df[f'{key}_unix'] = filtered_df[key].apply(OpsUtils.convert_time_unix)
            if isinstance(values, list):
                if len(values) == 2:
                    min_time = OpsUtils.convert_time_unix(values[0])
                    max_time = OpsUtils.convert_time_unix(values[1])
                    filtered_df = filtered_df[
                        (filtered_df[f'{key}_unix'] >= min_time) & 
                        (filtered_df[f'{key}_unix'] <= max_time)
                    ]
                else:
                    return -1  # invalid list length
            else:
                # Single date filtering
                filtered_df[f'{key}_date'] = filtered_df[f'{key}_unix'].apply(
                    lambda x: datetime.fromtimestamp(x, tz=timezone.utc).date()
                )
                target_date = datetime.strptime(values, "%Y-%m-%d").date()
                filtered_df = filtered_df[filtered_df[f'{key}_date'] == target_date]
        else:
            if isinstance(values, list):
                filtered_df = filtered_df[filtered_df[key].isin(values)]
            else:
                filtered_df = filtered_df[filtered_df[key] == values]

    filtered_uuid = list(filtered_df['uuid'])

    if displayIt:
        print('-- uuid --')
        display(filtered_uuid)
        print('-- Job Metadata --')
        display(filtered_df)

    return filtered_uuid, filtered_df