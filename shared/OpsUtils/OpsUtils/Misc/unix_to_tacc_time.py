def unix_to_tacc_time(unix_time):
    """
    Convert a Unix timestamp back into a TACC-style UTC timestamp string.

    Produces strings like:
        "2025-05-07T22:20:52.736325Z"

    Parameters
    ----------
    unix_time : float or int
        The Unix timestamp (seconds since epoch).

    Returns
    -------
    str
        A UTC timestamp string with 'Z' suffix.

    Example
    -------
    ts_str = unix_to_tacc_time(1751884852.736325)
    print(ts_str)
    # → "2025-05-07T22:20:52.736325Z"

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

    
    from datetime import datetime, timezone
    dt = datetime.fromtimestamp(unix_time, tz=timezone.utc)
    return dt.isoformat().replace('+00:00', 'Z')
