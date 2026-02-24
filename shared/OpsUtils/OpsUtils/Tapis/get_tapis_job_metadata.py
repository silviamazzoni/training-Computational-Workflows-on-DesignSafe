def get_tapis_job_metadata(t, jobUuid,printAll = True):
    """
    Retrieves and prints metadata for a specified Tapis job, including robust local archive reconstruction.

    This function queries the Tapis jobs API for metadata on a given job, printing
    details such as UUID, name, status, application ID, creation time, and archive location.

    If the job has completed successfully (status == 'FINISHED'), it reconstructs
    the expected local archive directory path under '~/MyData/tapis-jobs-archive',
    checks whether it exists, lists its contents, and returns this information
    in a structured dictionary.

    If the job is not yet finished or the local directory does not exist, it prints
    a notice and returns a dictionary describing the situation.

    Parameters
    ----------
    t : object
        An authenticated Tapis client instance (e.g., from `tapis3`).
    jobUuid : str
        UUID of the job whose metadata is to be retrieved.

    Returns
    -------
    dict
        A dictionary with the following keys:
        - "local_path" (str or None): local archive directory path if job is finished, else None.
        - "exists" (bool): True if the local directory exists.
        - "files" (list of str): list of files in the directory if it exists.
        - "message" (str, optional): explanatory message if no data is available.

    Prints
    ------
    - Job UUID, name, status, appId, creation time, and archive directory.
    - If finished, the reconstructed local archive path and the files contained within it,
      or a notice if the local directory does not exist.

    Example
    -------
    >>> result = get_tapis_job_metadata(t, "a1b2c3d4-5678-90ef-ghij-klmnopqrstuv")
    >>> if result["exists"]:
    ...     print("Archived job data at:", result["local_path"])
    ...     print("Files:", result["files"])
    ... else:
    ...     print(result.get("message", "Job not yet completed."))
    """

    # Silvia Mazzoni, 2025
    import os
    import json
    if printAll:
        import ipywidgets as widgets
        from IPython.display import display, clear_output
        metadata_out = widgets.Output()
        metadata_accordion = widgets.Accordion(children=[metadata_out])
        metadata_accordion.set_title(0, f'Job Metadata   ({jobUuid})')
        metadata_accordion.selected_index = 0
        display(metadata_accordion)

    job_response = t.jobs.getJob(jobUuid=jobUuid)
    job_dict_all = json.loads(json.dumps(job_response, default=lambda o: vars(o)))
    if printAll:
        with metadata_out:
            # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('+++++++++++++++++++++++++')
            print('++++++ Job Metadata')
            print('+++++++++++++++++++++++++')
    
            print('+ uuid:      ', job_response.uuid)
            print('+ name:      ', job_response.name)
            print('+ status:    ', job_response.status)
            print('+ appId:     ', job_response.appId)
            print('+ created:   ', job_response.created)
            print('+ output-file location')
            print('+ archiveSystemId:', job_response.archiveSystemId)
            print('+ archiveSystemDir:', job_response.archiveSystemDir)


    # ------
    execSystemId = job_response.execSystemId
    archiveSystemId = job_response.archiveSystemId
    sysPath = ''
    if archiveSystemId == 'designsafe.storage.default':
        sysPath = 'MyData'; 
    elif archiveSystemId in ['Work','work','cloud.data','stampede3',execSystemId]:
        sysPath = f'Work/{execSystemId}'; 
    if archiveSystemId == 'designsafe.storage.community':
        sysPath = 'CommunityData'; ## but you can't write to community
    if archiveSystemId == 'designsafe.storage.published':
        sysPath = 'Published'; ## but you can't write to published!
    
    archiveSystemDir = job_dict_all['archiveSystemDir']
    archiveSystemDir_user = archiveSystemDir.split('tapis-jobs-archive'+os.path.sep)[1] # remove the first character slash

    
    archiveSystemDir_user = os.path.join(sysPath,'tapis-jobs-archive',archiveSystemDir_user)
    
    archiveSystemDir_out = archiveSystemDir_user
    if job_response.appId in ["opensees-mp-s3","opensees-sp-s3"]:
        archiveSystemDir_out = os.path.join(archiveSystemDir_out,'inputDirectory')
    elif job_response.appId in ["opensees-express"]:
        fileInputsList =  json.loads(job_dict_all['fileInputs'])
        for fileInputs in fileInputsList:
            if fileInputs['name'] in ['Input Directory'] or fileInputs['envKey'] in ['inputDirectory']:
                sourceUrl = fileInputs['sourceUrl']
                input_folder_end = os.path.basename(sourceUrl)
                archiveSystemDir_out = os.path.join(archiveSystemDir_user,input_folder_end)
                break

    # if sysPath != '':
    archiveSystemDir_user = os.path.expanduser(os.path.join('~',archiveSystemDir_user))
    archiveSystemDir_out = os.path.expanduser(os.path.join('~',archiveSystemDir_out))

    
    job_dict_all['archiveSystemDir_user'] = archiveSystemDir_user
    job_dict_all['archiveSystemDir_out'] = archiveSystemDir_out
    
    if printAll:
        with metadata_out:
            print('+ archiveSystemDir_user:', job_dict_all['archiveSystemDir_user'])
            print('+ archiveSystemDir_out:', job_dict_all['archiveSystemDir_out'])

        
    
            JobInfoKeys = ['','uuid','name','','status','remoteOutcome','condition','lastMessage','','execSystemId','execSystemExecDir','execSystemOutputDir','','appId','appVersion','','tenant','trackingId','createdby','created','description','','execSystemId','execSystemLogicalQueue','nodeCount','coresPerNode','maxMinutes','memoryMB']
            
            # print('\n-- Additional Relevant Job Metadata --')
            print('+ ++++++++++++++++++++++++')
            print('+ +++++ Additional Relevant Job Metadata')
            print('+ ++++++++++++++++++++++++')
            for thisKey in JobInfoKeys:
                if thisKey in job_dict_all.keys():
                    thisValue = job_dict_all[thisKey]
                    # myJobTapisData[thisKey] = thisValue
                    print(f'+ - {thisKey}: {thisValue}')
                else:
                    print('+ ----------------------')
            print('+ ++++++++++++++++++++++++')
        if 'fileInputs' in job_dict_all.keys():

            this_out = widgets.Output()
            this_accordion = widgets.Accordion(children=[this_out])
            this_accordion.set_title(0, f'fileInputs')
            # this_accordion.selected_index = 0
            
            with metadata_out:
                display(this_accordion)
            with this_out:
            
                print('')
                print('#'*32)
                print('### fileInputs')
                print('#'*32)
                fileInputsList =  json.loads(job_dict_all['fileInputs'])
                for thisLine in fileInputsList:
                    print('# ' + '+'*30)
                    for thisKey,thisKeyVal in thisLine.items():
                        print(f'# + {thisKey} = {thisKeyVal}')
                    print('# ' + '+'*30)
                print('#'*32)
    
        if 'parameterSet' in job_dict_all.keys():

            this_out = widgets.Output()
            this_accordion = widgets.Accordion(children=[this_out])
            this_accordion.set_title(0, f'parameterSet')
            # this_accordion.selected_index = 0
            
            with metadata_out:
                display(this_accordion)
            with this_out:
                
                print('')
                print('#'*32)
                print('### parameterSet')
                print('#'*32)
                parameterSetDict =  json.loads(job_dict_all['parameterSet'])
                for thisLineKey,thisLineValues in parameterSetDict.items():
                    print('#')
                    print('# ' + '+'*30)
                    print(f'# ++ {thisLineKey} ')
                    print('# ' + '+'*30)
                    if isinstance(thisLineValues, list):
                        for thisLine in thisLineValues:
                            print('# ' + '+ ' + '-'*28)
                            if isinstance(thisLine, dict):
                                for thisKey,thisVal in thisLine.items():
                                    if thisVal != None:
                                        print(f'# + -  {thisKey} : {thisVal}')
                            else:
                                print('####################not dict',thisLine)
                            print('# ' + '+ ' + '-'*28)
                    elif isinstance(thisLineValues, dict):
                        for thisKey,thisVal in thisLineValues.items():
                            if thisVal != None:
                                print(f'# +  {thisKey} : {thisVal}')
                    else:
                        print('not list nor dict',thisLine)
                    print('# ' + '+'*30)
                print('#'*32)
        
    return job_dict_all
    




