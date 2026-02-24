def find_work_path(t, username):
    """
    Locate the full work directory path for a user in the Tapis 'cloud.data' system.

    On DesignSafe (and similar Tapis platforms), the 'Work' storage system is organized
    by allocation or project group directories under '/work', with user directories 
    nested inside (e.g., /work/05072/smazzoni). This function searches through these
    nested folders to find the user's specific work path.

    It does this by paging through batches of group directories, then checking inside
    each one for a folder matching the given username.

    Parameters
    ----------
    t : Tapis
        An authenticated Tapis client (from connect_tapis()).

    username : str
        The Tapis username to search for under the '/work' hierarchy.

    Returns
    -------
    FileListing
        The Tapis file object corresponding to the user's work directory,
        from which you can access .path and other metadata.

    Example
    -------
    work_file_object = find_work_path(t, username='smazzoni')
    print('Work path:', work_file_object.path)
    """
    # code by Silvia Mazzoni, 2025
    from tapipy.tapis import Tapis
    Offmax = 30
    foundit = False
    for i in range(1,Offmax):
        offset = i*1000
        # print('offset',offset)
        allWorkBase = t.files.listFiles(systemId='cloud.data', path='/work',offset=offset)
        icnt = 0
        for thisQ in allWorkBase:
            icnt+=1
            newName = thisQ.name
            hereWorkBase = t.files.listFiles(systemId='cloud.data', path=f'/work/{newName}')
            for hereQ in hereWorkBase:
                if hereQ.name==username:
                    foundit = True
                    workPath = hereQ.path
                    returnQ = hereQ
                    print('Found it!!!',workPath)
                    # print(returnQ)
                    break
        if icnt ==0 or foundit:
            break
        print(f'searched {offset+icnt} folders')
    return returnQ