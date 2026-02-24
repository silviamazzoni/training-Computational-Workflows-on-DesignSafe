def get_now_unix():
    """
    Get the current time as a Unix timestamp in UTC.

    Returns
    -------
    float
        Current time in seconds since the Unix epoch (1970-01-01 00:00:00 UTC).

    Example
    -------
    now = get_now_unix()
    print(f"Current Unix time: {now}")
    # → 1751234567.890123

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
    return datetime.now(timezone.utc).timestamp()
