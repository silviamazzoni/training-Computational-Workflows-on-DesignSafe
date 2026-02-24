def convert_time_unix(timestamp_str):
    """
    Convert a timestamp string (typically from Tapis or TACC job metadata) into a Unix timestamp.

    Automatically handles:
    - Full datetime strings with fractional seconds, e.g. "2025-05-07T22:20:52.736325Z"
    - Datetime strings without fractional seconds, e.g. "2025-05-07T22:20:52Z"
    - Simple date strings, e.g. "2025-05-07"

    Removes the 'Z' UTC suffix if present and always returns a UTC-based Unix time.

    Returns -1 if the input is empty, None, or if parsing fails.

    Parameters
    ----------
    timestamp_str : str
        A timestamp string in ISO format (with or without time).

    Returns
    -------
    float
        Unix timestamp in seconds (UTC), or -1 if conversion fails.

    Example
    -------
    ts = convert_time_unix("2025-05-07T22:20:52.736325Z")
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

    from datetime import datetime, timezone
    import re

    try:
        if not timestamp_str:
            return -1  # handle None or empty string

        is_utc = timestamp_str.endswith('Z')
        ts_clean = timestamp_str.rstrip('Z')
        if 'T' in ts_clean:
            if re.search(r'\.\d+', ts_clean):
                fmt = "%Y-%m-%dT%H:%M:%S.%f"
            else:
                fmt = "%Y-%m-%dT%H:%M:%S"
        else:
            fmt = "%Y-%m-%d"

        outTime = datetime.strptime(ts_clean, fmt)
        outTime = outTime.replace(tzinfo=timezone.utc)
        return outTime.timestamp()
    
    except Exception as e:
        print('There was an error in the format of you input:',timestamp_str)
        return -1
