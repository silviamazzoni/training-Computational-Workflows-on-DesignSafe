def queryDF(outKey, JobsData_df, key, values, displayIt=False):
    """
    Query a Pandas DataFrame to extract values from one column (outKey)
    where another column (key) matches specified values.

    This function checks that both specified columns exist, automatically
    wraps a single value into a list, filters the DataFrame, and returns
    the resulting list of values from the outKey column.

    If only one result is found, returns it as a scalar instead of a list.

    Parameters
    ----------
    outKey : str
        The column name to extract values from.

    JobsData_df : pandas.DataFrame
        The DataFrame to query.

    key : str
        The column name to filter on.

    values : list, set, tuple, or single value
        The values to filter by in the `key` column.

    displayIt : bool, default=False
        If True, prints a summary of the extracted values.

    Returns
    -------
    list or single value
        The extracted values from `outKey` for the matching rows.
        Returns a scalar if only one match.

    Example
    -------
    uuid_result = queryDF('uuid', filtered_df, 'index_column', 388, True)

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

    keyList = list(JobsData_df.keys())
    if not isinstance(values, (list, set, tuple)):
        values = [values]
    if not outKey in keyList:
        print(f'{outKey} is not a valid key for the dataframe! Please select from the following:',keyList)
        return []    
    if not key in JobsData_df.keys():
        print(f'{key} is not a valid key for the dataframe! Please select from the following:',keyList)
        return []
    thisOut = list(JobsData_df[JobsData_df[key].isin(values)][outKey])
    if len(thisOut)==1:
        thisOut = thisOut[0]
    if displayIt:
        print(f'outKey={thisOut}  for {key}={values}')
    return thisOut

# example:
# a=queryDF('uuid',filtered_df,'index_column',388,True)