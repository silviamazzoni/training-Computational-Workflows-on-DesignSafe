def find_work_path_path(t, username):
    """
    Quickly find and return the full absolute work path string for a user
    in the Tapis 'cloud.data' system (DesignSafe Work storage).

    This function wraps `find_work_path` and extracts just the `.path` attribute,
    giving you a clean string that you can use in file operations, job submissions,
    or path management scripts.

    Parameters
    ----------
    t : Tapis
        An authenticated Tapis client (from connect_tapis()).

    username : str
        The Tapis username whose work directory you want to locate.

    Returns
    -------
    str
        The absolute path string to the user's work directory, e.g.
        '/work/05072/smazzoni'.

    Example
    -------
    work_path = find_work_path_path(t, 'smazzoni')
    print('My Work directory is:', work_path)
    """

    # code by Silvia Mazzoni, 2025
    return find_work_path(t, username).path