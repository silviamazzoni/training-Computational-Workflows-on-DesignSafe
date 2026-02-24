def increment_tapis_app_version(t,app_id,updateType = 'patch'):
    from OpsUtils import OpsUtils
    results = t.apps.getApps()
    latest_app_version = OpsUtils.get_latest_app_version(t,app_id)
    if latest_app_version == 'none':
        print('new app')
        app_version = '0.0.1'
    else:
        print('app exists, now latest_app_version',latest_app_version)
        app_version = OpsUtils.bump_app_version(latest_app_version,updateType)
    print('now app_version',app_version)
    return app_version