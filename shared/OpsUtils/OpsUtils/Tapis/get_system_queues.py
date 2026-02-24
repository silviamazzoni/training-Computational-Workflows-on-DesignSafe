def get_system_queues(t, system_id="stampede3", display=True):
    """
    Retrieve and display the batch queues available on a given Tapis system.

    This function queries the system definition from Tapis, extracts the list of
    batch queues, builds a Pandas DataFrame for easy inspection, and optionally
    displays it in a transposed format (with queue names as columns).

    It also returns a dictionary keyed by queue name, so you can look up individual
    queue properties programmatically.

    Parameters
    ----------
    t : Tapis
        An authenticated Tapis client (from connect_tapis()).

    system_id : str, default="stampede3"
        The ID of the Tapis-registered system to query (such as "stampede3" on DesignSafe).

    display : bool, default=True
        If True, displays the transposed DataFrame of queues for easy exploration.

    Returns
    -------
    dict
        A dictionary where each key is a queue name and the value is a dictionary
        of that queue's properties.

    Example
    -------
    queues_info = get_system_queues(t, system_id="stampede3", display=True)
    print(queues_info["skx-normal"])
    """
    # code by Silvia Mazzoni, 2025
    import pandas as pd
    from tapipy.tapis import Tapis
    system_def = t.systems.getSystem(systemId=system_id)
    # Convert each TapisResult to a dictionary
    queue_dicts = [queue.__dict__ for queue in system_def.batchLogicalQueues]
    
    # Create the DataFrame
    queues_df = pd.DataFrame(queue_dicts)
    queues_df.set_index('name', inplace=True)
    
    # Optional: display the DataFrame nicely
    from IPython.display import display
    # display(queues_df)
    
    transposed_df = queues_df.T
    if display:
        display(transposed_df)
    # Return as dictionary keyed by queue name
    return {q["name"]: q for q in queue_dicts}
