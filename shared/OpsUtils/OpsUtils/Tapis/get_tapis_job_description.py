# /home/jupyter/CommunityData/OpenSees/TrainingMaterial/training-OpenSees-on-DesignSafe/OpsUtils/OpsUtils/Tapis/get_tapis_job_description.py
def get_tapis_job_description(t, tapisInput):
    """
    Build a complete Tapis v3 job description dict from user-friendly inputs.

    This function:
      1) Resolves the Files base URL for inputs from `tapisInput["storage_system"]`
         (supports MyData/community/published; can be overridden via
         `tapisInput["storage_system_baseURL"]`).
      2) Ensures a concrete application version:
         - If `appVersion` is missing or equals "latest", it resolves a pinned
           version via `OpsUtils.get_latest_app_version(t, )`.
      3) Validates required fields (set differs for OpenSees-Express vs. HPC apps).
      4) Constructs job attributes, fileInputs, parameterSet, and archive settings.

    Auto baseURL selection
    ----------------------
    If `storage_system_baseURL` is not provided:
      - If `storage_system` contains "mydata": uses
        `tapis://designsafe.storage.default/` where `` is taken
        from `t.authenticator.get_userinfo().username`.
      - If `storage_system` contains "community": uses
        `tapis://designsafe.storage.community`
      - If `storage_system` contains "published": uses
        `tapis://designsafe.storage.published`
      - Else: prints a message and returns -1.

    App families and required keys
    ------------------------------
    *OpenSees-Express* (`appId == "opensees-express"`)
      Required: ['name','appId','appVersion','maxMinutes','archive_system',
                 'storage_system','input_folder','Main Script']
      - Sets `parameterSet.envVariables` with:
          mainProgram = OpenSees
          tclScript   = 

      - `fileInputs = [{"name": "Input Directory", "sourceUrl": "/"}]`
      - Archive options:
          archive_system == 'MyData' -> designsafe.storage.default under
              ${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}
          archive_system == 'Temp'   -> cloud.data:/tmp/${JobOwner}/tapis-jobs-archive/...

    *HPC OpenSees apps* (e.g., opensees-mp-s3, opensees-sp-*, etc.)
      Required: ['name','appId','appVersion','execSystemId','execSystemLogicalQueue',
                 'nodeCount','coresPerNode','maxMinutes','allocation','archive_system',
                 'storage_system','input_folder','Main Script']
      - Sets base job attributes (system, queue, resources).
      - `parameterSet.appArgs = [{"name": "Main Script", "arg": 
}]`
      - `parameterSet.schedulerOptions = [{"name": "TACC Allocation",
                                           "arg": f"-A {allocation}"}]`
      - `fileInputs` as above.
      - Archive options:
          archive_system == 'MyData' -> designsafe.storage.default under
              ${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}
          archive_system == 'Work'   -> exec system $WORK/tapis-jobs-archive/...

    Returns
    -------
    dict
        A fully formed Tapis job description ready for submission.
        Returns -1 if validation fails or baseURL/appVersion cannot be determined.

    Side effects
    ------------
    - Prints a list of missing required keys (if any).
    - Prints a short confirmation ("All Input is Complete") on success.

    Author
    ------
    Silvia Mazzoni, DesignSafe (silviamazzoni@yahoo.com)

    Date
    ----
    2025-08-16

    Version
    -------
    1.2
    """
    # Silvia Mazzoni, 2025
    from OpsUtils import OpsUtils  # for get_latest_app_version

    def checkRequirements(tapisInputIN, RequiredInputList):
        nmiss = 0
        for thisReq in RequiredInputList:
            if thisReq not in tapisInputIN.keys():
                nmiss += 1
                print(f"YOU need to define the following input: {thisReq}")
        return nmiss


    def processAppDictList(app_DictList,tapisInputIN,kwPairabels):
        [nameLabel,valueLabel] = kwPairabels
        here_dict_list = []
        for app_Dict in app_DictList:
            app_Dict = app_Dict.__dict__
            here_name = app_Dict[nameLabel]
            here_value = app_Dict[valueLabel]
            # input_name = app_Dict[inputLabel]

            if 'notes' in app_Dict.keys():
                app_Dict_notes = app_Dict['notes'].__dict__
                if 'isHidden' in app_Dict_notes.keys() and app_Dict_notes['isHidden']==True:
                    continue
            here_inputMode = app_Dict['inputMode']
            if here_inputMode == 'FIXED':
                continue
            if here_name in tapisInputIN.keys():
                here_value = tapisInputIN[here_name]
            else:
                if here_inputMode == 'REQUIRED':
                    if here_value == None:
                        print(f'error 101 -- You need to specify {here_name} in your Tapis Input. {tapisInputIN.keys()}')
                        return -1
            if here_value != None:
                # here_value = ''
                here_dict= {nameLabel:here_name,valueLabel:here_value}
                # print('-----here_dict',here_dict)
                here_dict_list.append(here_dict)
        return here_dict_list

    appId = tapisInput["appId"]
    if checkRequirements(tapisInput, ["appId"])>0:
        return -1

    # --- Defaults & branching ---
    defaults = {'name':tapisInput["appId"]}
    for thisKey,thisDefaultValue in defaults.items():
        if thisKey not in tapisInput.keys():
            tapisInput[thisKey] = thisDefaultValue

    # --- Ensure a concrete appVersion (resolve 'latest' or missing) ---
    if ("appVersion" not in tapisInput.keys()) or (str(tapisInput["appVersion"]).lower() == "latest"):
        resolved = OpsUtils.get_latest_app_version(t, appId)
        if not resolved or resolved in ("none", ""):
            print(f"Unable to resolve latest version for appId='{appId}'. Please specify appVersion.")
            return -1
        tapisInput["appVersion"] = resolved


    # INITIALIZE
    job_description = {}        
    job_description["name"] = tapisInput["name"]
    job_description["appId"] = tapisInput["appId"]
    job_description["appVersion"] = tapisInput["appVersion"]
    if len(job_description["name"])>64:
        job_description["name"] = job_description["name"][0:64]

    # --- Get App Schema ---
    appMetaData = t.apps.getAppLatestVersion(appId=appId)
    app_MetaData = appMetaData.__dict__
    app_jobAttributes = app_MetaData['jobAttributes'].__dict__
    
    app_fileInputs = app_jobAttributes['fileInputs']
    app_parameterSet = app_jobAttributes['parameterSet'].__dict__
    # app_parameterSet_appArgs = app_parameterSet['appArgs'].__dict__
    # app_parameterSet_schedulerOptions = app_parameterSet['schedulerOptions'].__dict__
    # app_parameterSet_envVariables = app_parameterSet['envVariables'].__dict__

    if appId == "opensees-express" and "mainProgram" not in tapisInput.keys() and "Main Program" in tapisInput.keys():
        tapisInput["mainProgram"] = tapisInput["Main Program"]

    UnprocessableJobAttrKeys = ['fileInputArrays']
    UnprocessableParamSetKeys = ['containerArgs']

    
    kwPair = {}
    kwPair['appArgs'] = ['name','arg']
    kwPair['envVariables'] = ['key','value']
    kwPair['schedulerOptions'] = ['name','arg']
    
    for thisJobAttrKey,thisJobAttrAppValue in app_jobAttributes.items():
        if thisJobAttrKey in UnprocessableJobAttrKeys and len(thisJobAttrAppValue)>0:
            print(f"I (def get_tapis_job_description) don't know how to interpret this jobAttribute:",thisJobAttrKey)
        elif thisJobAttrKey == 'fileInputs':
            # --- Resolve storage baseURL if needed ---
            print('fileInputs')
            job_description[thisJobAttrKey] = []
            if len(app_fileInputs)>0:
                
                for thisAppFileInput in app_fileInputs:
                    # print('thisAppFileInput',thisAppFileInput)
                    thisAppFileInput = thisAppFileInput.__dict__
                    if 'notes' in thisAppFileInput.keys():
                        app_Dict_notes = thisAppFileInput['notes'].__dict__
                        if 'isHidden' in app_Dict_notes and app_Dict_notes['isHidden']==True:
                            continue
                    if 'sourceUrl' in thisAppFileInput.keys():
                         # print('sourceUrl in thisAppFileInput')
                        if "sourceUrl" not in tapisInput.keys():
                            # print('sourceUrl not in tapisInput')
                            if "storage_system_baseURL" not in tapisInput.keys():
                                if 'storage_system' not in tapisInput.keys():
                                    if 'sourceUrl' not in thisAppFileInput.keys() and thisAppFileInput['inputMode']=='REQUIRED':
                                        tapisInput['storage_system'] = 'MyData'
                                        print(f"I (def get_tapis_job_description) set your 'storage_system' to default value {tapisInput['storage_system']}")
                                        # return -1
                                storage_system_lower = tapisInput.get("storage_system", "").lower()
                                tapisInput['storage_system_baseURL'] = OpsUtils.get_user_path_tapis_uri(t,storage_system_lower)

                            tapisInput["sourceUrl"] = f"{tapisInput['storage_system_baseURL']}"
                            if 'input_folder' in tapisInput.keys():
                                tapisInput["sourceUrl"] = f"{tapisInput['sourceUrl']}/{tapisInput['input_folder']}"
                        print('sourceurl',tapisInput["sourceUrl"])
                        hereFileInput = {"name":thisAppFileInput["name"],"sourceUrl": tapisInput["sourceUrl"]}
                        print('hereFileInput',hereFileInput)
                    else:
                        print(f"I (def get_tapis_job_description) don't know how to interpret this {thisJobAttrKey}:",thisAppFileInput)
                        hereFileInput = thisAppFileInput
                        
                    job_description[thisJobAttrKey].append(hereFileInput)
                
                if 'sourceUrl' in tapisInput.keys():
                    print('input directory URI (sourceUrl):',tapisInput["sourceUrl"])
        elif thisJobAttrKey == 'parameterSet':
            job_description[thisJobAttrKey] = {}
            thisJobAttrAppValueDict = thisJobAttrAppValue.__dict__
            for thisParamSetKey,thisParamSetAppValue in thisJobAttrAppValueDict.items():
                if thisParamSetKey in UnprocessableParamSetKeys and len(thisParamSetAppValue)>0:
                    print(f"I (def get_tapis_job_description) don't know how to interpret this {thisJobAttrKey}:",thisParamSetKey)
                    
                elif thisParamSetKey in ['appArgs','envVariables','schedulerOptions']:
                    job_description[thisJobAttrKey][thisParamSetKey] = []
                    kwPairabels = kwPair[thisParamSetKey]
                    hereDictList = processAppDictList(thisParamSetAppValue,tapisInput,kwPairabels)
                    if hereDictList == -1:
                        return -1
                    job_description[thisJobAttrKey][thisParamSetKey] = hereDictList                    
                    if thisParamSetKey == 'schedulerOptions':
                        if 'allocation' in tapisInput.keys():
                            AllocationDict = {"name": "TACC Allocation", "arg": f"-A {tapisInput['allocation']}"}
                            job_description[thisJobAttrKey][thisParamSetKey].append(AllocationDict)
                        if 'Allocation' in tapisInput.keys():
                            AllocationDict = {"name": "TACC Allocation", "arg": f"-A {tapisInput['Allocation']}"}
                            job_description[thisJobAttrKey][thisParamSetKey].append(AllocationDict)
        else:
            if thisJobAttrKey in tapisInput.keys():
                job_description[thisJobAttrKey] = tapisInput[thisJobAttrKey]
            else:
                if thisJobAttrAppValue!=None:
                    job_description[thisJobAttrKey] = thisJobAttrAppValue
                

        
    
    # If Express, default the exec system to the Express VM unless provided
    if appId == "opensees-express" and "execSystemId" not in tapisInput.keys():
        job_description["execSystemId"] = "wma-exec-01"


        
    # Archive location
    if "archive_system" in tapisInput:
        if tapisInput["archive_system"] == "MyData":
            job_description["archiveSystemId"] = "designsafe.storage.default"
            job_description["archiveSystemDir"] = "${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}"
        elif tapisInput["archive_system"] == "Work" and tapisInput["execSystemId"] != "wma-exec-01":
            job_description["archiveSystemId"] = tapisInput["execSystemId"]
            job_description["archiveSystemDir"] = "HOST_EVAL($WORK)/tapis-jobs-archive/${JobCreateDate}/${JobName}-${JobUUID}"
        else:
            job_description["archiveSystemId"] = "designsafe.storage.default"
            job_description["archiveSystemDir"] = "${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}"
    else:
        job_description["archiveSystemId"] = "designsafe.storage.default"
        job_description["archiveSystemDir"] = "${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}"

    # display(job_description)

    return job_description