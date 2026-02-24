def query_tapis_apps(t,idquery=[],version='',select=''):
    # by Silvia Mazzoni, 2025
    # examples:
    # results = query_tapis_apps(t,['opensees','mp'],version='latest',select = 'id,created,description,version')    
    # results = query_tapis_apps(t,['opensees','mp'],select = 'id,created,description,version')
    # results = query_tapis_apps(t,['opensees','mp'],version='latest')    
    # results = query_tapis_apps(t,['opensees','sp'])
    

    listType = 'ALL'
    
    inputs = [t]
    searchQuery = ''
    if len(idquery)>0:
        searchQuery = "id.like.*"
        for thisQ in idquery:
            searchQuery += f"{thisQ}*"
        
    if len(version)>0:
        endstr = ''
        if len(searchQuery)>0:
            searchQuery = f'({searchQuery})~('
            endstr = ')'
        searchQuery += f'version.eq.{version}'
        searchQuery += endstr
    results = t.apps.getApps(search=searchQuery,
                listType=listType,select=select)
    return results