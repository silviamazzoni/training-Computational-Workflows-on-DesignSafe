# def get_tapis_job_description_agnostic(t, tapisInput):
#     """
#     Build a complete Tapis v3 job description dict from user-friendly inputs.

#     This function:
#       1) Resolves the Files base URL for inputs from `tapisInput["storage_system"]`
#          (supports MyData/community/published; can be overridden via
#          `tapisInput["storage_system_baseURL"]`).
#       2) Ensures a concrete application version:
#          - If `appVersion` is missing or equals "latest", it resolves a pinned
#            version via `OpsUtils.get_latest_app_version(t, <appId>)`.
#       3) Validates required fields (set differs for OpenSees-Express vs. HPC apps).
#       4) Constructs job attributes, fileInputs, parameterSet, and archive settings.

#     Auto baseURL selection
#     ----------------------
#     If `storage_system_baseURL` is not provided:
#       - If `storage_system` contains "mydata": uses
#         `tapis://designsafe.storage.default/<username>` where `<username>` is taken
#         from `t.authenticator.get_userinfo().username`.
#       - If `storage_system` contains "community": uses
#         `tapis://designsafe.storage.community`
#       - If `storage_system` contains "published": uses
#         `tapis://designsafe.storage.published`
#       - Else: prints a message and returns -1.

#     App families and required keys
#     ------------------------------
#     *OpenSees-Express* (`appId == "opensees-express"`)
#       Required: ['name','appId','appVersion','maxMinutes','archive_system',
#                  'storage_system','input_folder','Main Script']
#       - Sets `parameterSet.envVariables` with:
#           mainProgram = OpenSees
#           tclScript   = <Main Script>
#       - `fileInputs = [{"name": "Input Directory", "sourceUrl": "<base>/<input_folder>"}]`
#       - Archive options:
#           archive_system == 'MyData' -> designsafe.storage.default under
#               ${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}
#           archive_system == 'Temp'   -> cloud.data:/tmp/${JobOwner}/tapis-jobs-archive/...

#     *HPC OpenSees apps* (e.g., opensees-mp-s3, opensees-sp-*, etc.)
#       Required: ['name','appId','appVersion','execSystemId','execSystemLogicalQueue',
#                  'nodeCount','coresPerNode','maxMinutes','allocation','archive_system',
#                  'storage_system','input_folder','Main Script']
#       - Sets base job attributes (system, queue, resources).
#       - `parameterSet.appArgs = [{"name": "Main Script", "arg": <Main Script>}]`
#       - `parameterSet.schedulerOptions = [{"name": "TACC Allocation",
#                                            "arg": f"-A {allocation}"}]`
#       - `fileInputs` as above.
#       - Archive options:
#           archive_system == 'MyData' -> designsafe.storage.default under
#               ${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}
#           archive_system == 'Work'   -> exec system $WORK/tapis-jobs-archive/...

#     Returns
#     -------
#     dict
#         A fully formed Tapis job description ready for submission.
#         Returns -1 if validation fails or baseURL/appVersion cannot be determined.

#     Side effects
#     ------------
#     - Prints a list of missing required keys (if any).
#     - Prints a short confirmation ("All Input is Complete") on success.

#     Author
#     ------
#     Silvia Mazzoni, DesignSafe (silviamazzoni@yahoo.com)

#     Date
#     ----
#     2025-08-16

#     Version
#     -------
#     1.2
#     """
#     # Silvia Mazzoni, 2025
#     from OpsUtils import OpsUtils  # for get_latest_app_version

#     def checkRequirements(tapisInputIN, RequiredInputList):
#         nmiss = 0
#         for thisReq in RequiredInputList:
#             if thisReq not in tapisInputIN:
#                 nmiss += 1
#                 print(f"YOU need to define the following input: {thisReq}")
#         return nmiss

#     # --- Resolve storage baseURL if needed ---
#     if "storage_system_baseURL" not in tapisInput:
#         storage_system_lower = tapisInput.get("storage_system", "").lower()
#         if "mydata" in storage_system_lower:
#             # Get user information for MyData path
#             user_info = t.authenticator.get_userinfo()
#             username = user_info.username
#             tapisInput["storage_system_baseURL"] = f"tapis://designsafe.storage.default/{username}"
#         elif "community" in storage_system_lower:
#             tapisInput["storage_system_baseURL"] = "tapis://designsafe.storage.community"
#         elif "published" in storage_system_lower:
#             tapisInput["storage_system_baseURL"] = "tapis://designsafe.storage.published"
#         else:
#             print("Please specify tapisInput['storage_system_baseURL']!")
#             return -1

#     sourceUrl = f"{tapisInput['storage_system_baseURL']}/{tapisInput['input_folder']}"

#     appId = tapisInput["appId"]
#     # print('appId',appId)

#     # --- Ensure a concrete appVersion (resolve 'latest' or missing) ---
#     if ("appVersion" not in tapisInput) or (str(tapisInput["appVersion"]).lower() == "latest"):
#         resolved = OpsUtils.get_latest_app_version(t, appId)
#         if not resolved or resolved in ("none", ""):
#             print(f"Unable to resolve latest version for appId='{appId}'. Please specify appVersion.")
#             return -1
#         tapisInput["appVersion"] = resolved


#     # --- Defaults & branching ---
#     # If Express, default the exec system to the Express VM unless provided
#     if appId == "opensees-express" and "execSystemId" not in tapisInput:
#         tapisInput["execSystemId"] = "wma-exec-01"
#     if "execSystemId" not in tapisInput:
#         tapisInput["execSystemId"] = "stampede3"

#     job_description = {}
#     nmiss = 999

#     # Express (runs on wma-exec-01)
#     if appId == "opensees-express":
#         RequiredInputList = [
#             "name", "appId", "maxMinutes", "archive_system",
#             "storage_system", "input_folder", "Main Script"
#         ]
#         nmiss = checkRequirements(tapisInput, RequiredInputList)
#         if nmiss == 0:
#             parameterSet = {}
#             job_description["name"] = tapisInput["name"]
#             job_description["maxMinutes"] = tapisInput["maxMinutes"]
#             job_description["appId"] = tapisInput["appId"]
#             if 'appVersion' in tapisInput.keys():
#                 job_description["appVersion"] = tapisInput["appVersion"]
#             fileInputs = [{"name": "Input Directory", "sourceUrl": sourceUrl}]
#             if not 'Main Program' in tapisInput.keys():
#                 tapisInput["Main Program"] = 'OpenSees'
#             parameterSet["envVariables"] = [
#                 {"key": "mainProgram", "value": tapisInput["Main Program"]},
#                 {"key": "tclScript", "value": tapisInput["Main Script"]},
#             ]
#             job_description["fileInputs"] = fileInputs
#             job_description["parameterSet"] = parameterSet

#             # Archive location
#             if "archive_system" in tapisInput:
#                 if tapisInput["archive_system"] in ["MyData"]:
#                     job_description["archiveSystemId"] = "designsafe.storage.default"
#                     job_description["archiveSystemDir"] = "${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}"
#                 elif tapisInput["archive_system"] == "Temp":
#                     job_description["archiveSystemId"] = "cloud.data"
#                     job_description["archiveSystemDir"] = "/tmp/${JobOwner}/tapis-jobs-archive/${JobCreateDate}/${JobName}-${JobUUID}"
#             else:
#                 # default to MyData
#                 job_description["archiveSystemId"] = "designsafe.storage.default"
#                 job_description["archiveSystemDir"] = "${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}"

#     else:
#         # HPC (e.g., OpenSeesMP/SP on Stampede3)
#         RequiredInputList = [
#             "name","appId","execSystemId","execSystemLogicalQueue",
#             "nodeCount","coresPerNode","maxMinutes","allocation","archive_system",
#             "storage_system","input_folder","Main Script"
#         ]
#         nmiss = checkRequirements(tapisInput, RequiredInputList)
#         if nmiss == 0:
#             parameterSet = {}
#             job_description["name"] = tapisInput["name"]
#             job_description["execSystemId"] = tapisInput["execSystemId"]
#             job_description["execSystemLogicalQueue"] = tapisInput["execSystemLogicalQueue"]
#             job_description["maxMinutes"] = tapisInput["maxMinutes"]
#             job_description["nodeCount"] = tapisInput["nodeCount"]
#             job_description["coresPerNode"] = tapisInput["coresPerNode"]
#             job_description["appId"] = tapisInput["appId"]
#             if 'appVersion' in tapisInput.keys():
#                 job_description["appVersion"] = tapisInput["appVersion"]
#             fileInputs = [{"name": "Input Directory", "sourceUrl": sourceUrl}]
#             if not 'Main Program' in tapisInput.keys():
#                 tapisInput["Main Program"] = 'OpenSeesMP'
#             if not 'CommandLine Arguments' in tapisInput:
#                 tapisInput["CommandLine Arguments"] = ''
#             parameterSet["appArgs"] = [{"name": "Main Program", "arg": tapisInput["Main Program"]},
#                                        {"name": "Main Script", "arg": tapisInput["Main Script"]},
#                                        {"name": "CommandLine Arguments", "arg": tapisInput["CommandLine Arguments"]}
#                                       ]
#             parameterSet["envVariables"] = []
#             parameterSet["schedulerOptions"] = [{"name": "TACC Allocation", "arg": f"-A {tapisInput['allocation']}"}]
#             job_description["fileInputs"] = fileInputs
#             job_description["parameterSet"] = parameterSet

#             # # Archive location
#             # if "archive_system" in tapisInput:
#             #     if tapisInput["archive_system"] == "MyData":
#             #         job_description["archiveSystemId"] = "designsafe.storage.default"
#             #         job_description["archiveSystemDir"] = "${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}"
#             #     elif tapisInput["archive_system"] == "Work":
#             #         job_description["archiveSystemId"] = tapisInput["execSystemId"]
#             #         job_description["archiveSystemDir"] = "HOST_EVAL($WORK)/tapis-jobs-archive/${JobCreateDate}/${JobName}-${JobUUID}"

#     if nmiss == 0:
#         # Archive location
#         if "archive_system" in tapisInput:
#             if tapisInput["archive_system"] == "MyData":
#                 job_description["archiveSystemId"] = "designsafe.storage.default"
#                 job_description["archiveSystemDir"] = "${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}"
#             elif tapisInput["archive_system"] == "Work" and tapisInput["execSystemId"] != "wma-exec-01":
#                 job_description["archiveSystemId"] = tapisInput["execSystemId"]
#                 job_description["archiveSystemDir"] = "HOST_EVAL($WORK)/tapis-jobs-archive/${JobCreateDate}/${JobName}-${JobUUID}"
#             else:
#                 job_description["archiveSystemId"] = "designsafe.storage.default"
#                 job_description["archiveSystemDir"] = "${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}"

#         else:
#             job_description["archiveSystemId"] = "designsafe.storage.default"
#             job_description["archiveSystemDir"] = "${EffectiveUserId}/tapis-jobs-archive/${JobCreateDate}/${JobUUID}"

#     if nmiss == 0:
#         for envVar in ['zipFileIn','zipFolderOut']:
#             if envVar in tapisInput:
#                 job_description["parameterSet"]['envVariables'].append({"key": envVar, "value": tapisInput[envVar]})
                

#     # --- Finalize ---
#     if nmiss > 0:
#         print("Please resubmit with all required input")
#         return -1
#     else:
#         # print("All Input is Complete")
#         return job_description
