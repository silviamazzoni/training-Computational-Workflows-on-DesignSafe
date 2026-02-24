def convert_tacc_time(timestamp_str):
    """
    Convert a TACC-style UTC timestamp string into a Unix timestamp.

    This function parses timestamp strings in the format typically returned
    by Tapis or DesignSafe job metadata, such as:
        "2025-05-07T22:20:52.736325Z"
    and converts it into seconds since epoch (1970-01-01 UTC).

    Parameters
    ----------
    timestamp_str : str
        A UTC timestamp string ending in 'Z'.

    Returns
    -------
    float
        The corresponding Unix timestamp.

    Example
    -------
    ts = convert_tacc_time("2025-05-07T22:20:52.736325Z")
    print(ts)  # → 1751884852.736325

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

    from datetime import datetime
    dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    unix_time = dt.timestamp()
    return unix_time
