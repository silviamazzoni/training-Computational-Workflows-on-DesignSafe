def establish_tms_credentials(tapis, system_id: str, username: str):
    """
    Ensure that a user has valid TMS (Tapis Managed System) credentials on a given system.

    This function checks if the specified user already has credentials (such as TMS_KEYS) 
    registered on the specified Tapis system. If the credentials are missing, it 
    automatically establishes them (for systems that use TMS_KEYS authentication).

    This is essential for enabling file operations, data transfers, and job submissions
    that require user-level credentials on systems like DesignSafe storage.

    Parameters
    ----------
    tapis : Tapis
        An authenticated Tapis client (from connect_tapis()).

    system_id : str
        The ID of the Tapis-registered system (e.g. 'designsafe.storage.default').

    username : str
        The Tapis username for which to check or establish credentials.

    Returns
    -------
    None
        Prints status messages indicating whether credentials were found or established.

    Example
    -------
    establish_tms_credentials(
        tapis, 
        system_id='designsafe.storage.default', 
        username='smazzoni'
    )
    """
    # Silvia Mazzoni, 2025
    print(" -- TMS User Credentials --")
    """
    Check if user has system credentials on system.
    If not, it will set them.
    """
    from tapipy.errors import UnauthorizedError
    print('username:',username)
    print('system_id:',system_id)
    try:
        tapis.systems.checkUserCredential(systemId=system_id, userName=username)
        print(f"Found {username}'s system credentials.")
        return
    except UnauthorizedError:
        print(f"User {username} is missing system credentials.")
        print(f"Establishing new credentials")
        system_def = tapis.systems.getSystem(systemId=system_id)
        if system_def.get("defaultAuthnMethod") == "TMS_KEYS":
            tapis.systems.createUserCredential(
                systemId=system_id,
                userName=username,
                createTmsKeys=True,
            )
        print(f"Established {username}'s system credentials.")
    print('-- CREDENTIALS ESTABLISHED SUCCESSFULLY!!! --')
