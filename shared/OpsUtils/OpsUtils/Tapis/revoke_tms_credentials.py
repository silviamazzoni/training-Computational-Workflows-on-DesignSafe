def revoke_tms_credentials(tapis, system_id: str, username: str):
    """
    Remove TMS (Tapis Managed System) credentials for a user on a given system.

    This function deletes the stored user credentials on the specified Tapis system,
    which is useful for resetting or cleaning up keys, especially on systems that use
    TMS_KEYS authentication (like DesignSafe storage systems).

    Parameters
    ----------
    tapis : Tapis
        An authenticated Tapis client (from connect_tapis()).

    system_id : str
        The ID of the Tapis-registered system (e.g. 'designsafe.storage.default').

    username : str
        The Tapis username whose credentials will be removed.

    Returns
    -------
    None
        Prints a confirmation message when credentials are successfully removed.

    Example
    -------
    remove_tms_credentials(tapis, system_id='designsafe.storage.default', username='smazzoni')
    """
    # Silvia Mazzoni, 2025
    tapis.systems.removeUserCredential(systemId=system_id, userName=username)
    print('-- CREDENTIALS REMOVED SUCCESSFULLY!!! --')