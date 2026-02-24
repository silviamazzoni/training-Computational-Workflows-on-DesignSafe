# app.json

Here's a **detailed walkthrough of each field** in the *app.json* file for the *OpenSees-express* Tapis App.

https://github.com/TACC/WMA-Tapis-Templates/blob/main/applications/opensees-express/app.json

##  App-Definition File
:::{dropdown} **app.json**
The following json was copied from github and may have changed.
```
{
    "id": "opensees-express",
    "version": "latest",
    "description": "OpenSees-EXPRESS provides users with a sequential OpenSees interpreter. It is ideal to run small sequential scripts on DesignSafe resources freeing up your own machine.",
    "owner": "${apiUserId}",
    "enabled": true,
    "runtime": "ZIP",
    "runtimeVersion": null,
    "runtimeOptions": null,
    "containerImage": "tapis://cloud.data/corral/tacc/aci/CEP/applications/v3/opensees/latest/OpenSees-EXPRESS/opensees_express.zip",
    "jobType": "FORK",
    "maxJobs": -1,
    "maxJobsPerUser": -1,
    "strictFileInputs": true,
    "jobAttributes": {
        "execSystemConstraints": null,
        "execSystemId": "wma-exec-01",
        "execSystemExecDir": "${JobWorkingDir}",
        "execSystemInputDir": "${JobWorkingDir}",
        "execSystemOutputDir": "${JobWorkingDir}",
        "execSystemLogicalQueue": null,
        "archiveSystemId": "cloud.data",
        "archiveSystemDir": "/tmp/${JobOwner}/tapis-jobs-archive/${JobCreateDate}/${JobName}-${JobUUID}",
        "archiveOnAppError": true,
        "isMpi": false,
        "mpiCmd": null,
        "cmdPrefix": null,
        "parameterSet": {
            "appArgs": [],
            "containerArgs": [],
            "schedulerOptions": [],
            "envVariables": [
                {
                    "key": "mainProgram",
                    "value": "OpenSees",
                    "description": "Choose the OpenSees binary to use.",
                    "inputMode": "REQUIRED",
                    "notes": {
                        "label": "Main Program",
                        "enum_values": [
                            {
                                "OpenSees": "OpenSees"
                            },
                            {
                                "OpenSeesSP": "OpenSeesSP"
                            },
                            {
                                "OpenSeesMP": "OpenSeesMP"
                            }
                        ]
                    }
                },
                {
                    "key": "tclScript",
                    "value": "",
                    "description": "The filename of the OpenSees TCL script to execute, e.g. \"freeFieldEffective.tcl\".",
                    "inputMode": "REQUIRED",
                    "notes": {
                        "label": "Main Script",
                        "inputType": "fileInput"
                    }
                }
            ],
            "archiveFilter": {
                "includes": [],
                "excludes": [
                    "opensees-express.zip",
                    "tapisjob.env"
                ],
                "includeLaunchFiles": true
            }
        },
        "fileInputs": [
            {
                "name": "Input Directory",
                "inputMode": "REQUIRED",
                "sourceUrl": null,
                "targetPath": "*",
                "envKey": "inputDirectory",
                "description": "Input directory that includes the tcl script as well as any other required files. Example input is in tapis://designsafe.storage.community/app_examples/opensees/OpenSeesEXPRESS",
                "notes": {
                    "selectionMode": "directory"
                }
            }
        ],
        "fileInputArrays": [],
        "maxMinutes": 1440,
        "subscriptions": [],
        "tags": []
    },
    "tags": [
        "portalName: DesignSafe",
        "portalName: CEP"
    ],
    "notes": {
        "label": "OpenSees-EXPRESS (VM)",
        "helpUrl": "https://www.designsafe-ci.org/user-guide/tools/simulation/#opensees-user-guide",
        "hideNodeCountAndCoresPerNode": true,
        "isInteractive": false,
        "icon": "OpenSees",
        "category": "Simulation"
    }
}
```
:::


## App-Definition Arguments

:::{dropdown} Basic App Metadata
| Field         | Purpose                                                                                                 |
| ------------- | ------------------------------------------------------------------------------------------------------- |
| *id*          | Unique identifier for this app within Tapis (e.g., *"opensees-express"*)                                |
| *version*     | Version string (e.g., *"latest"*) — multiple versions can be registered under the same *id*             |
| *description* | A short user-facing explanation of what the app does                                                    |
| *owner*       | The Tapis user ID that owns this app (in this case, a variable *${apiUserId}* used during registration) |
| *enabled*     | Whether the app is active and visible for use                                                           |
:::


:::{dropdown} Runtime & Container Setup
| Field                       | Purpose                                                                                                          |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| *runtime*                   | Set to *"ZIP"* — this tells Tapis to unpack a ZIP archive that contains the container image and supporting files |
| *containerImage*            | Tapis path to the zipped runtime package (this is hosted in the TACC *cloud.data* system)                        |
| *jobType*                   | *"FORK"* means the app runs as a standard forked process (not MPI or batch-script based)                         |
| *maxJobs*, *maxJobsPerUser* | Limits on concurrent job submissions (−1 means unlimited)                                                        |
| *strictFileInputs*          | If *true*, only declared input files can be staged; prevents undeclared files from being uploaded                |
:::


## jobAttributes: Job-Execution Attributes
:::{dropdown} Job-Execution Metadata
This section controls how and where the job is run:

| Field                                        | Purpose                                                                                     |
| -------------------------------------------- | ------------------------------------------------------------------------------------------- |
| *execSystemId*                               | The registered Tapis system (here, *"wma-exec-01"*) where jobs will run                     |
| *execSystemExecDir*, *InputDir*, *OutputDir* | All point to *${JobWorkingDir}* so everything happens in the same job folder                |
| *archiveSystemId*                            | Where results are stored after the job finishes (here, *cloud.data*)                        |
| *archiveSystemDir*                           | Path format for archived output, with dynamic variables like *${JobOwner}* and *${JobUUID}* |
| *archiveOnAppError*                          | Whether outputs should still be archived even if the job errors out (*true*)                |
| *isMpi*                                      | Set to *false* because this app does not use MPI                                            |
| *maxMinutes*                                 | Max walltime allowed (in minutes); *1440* = 24 hours                                        |
:::

###  jobAttributes.parameterSet.envVariables

These are **app parameters** passed as environment variables:
    
:::{dropdown} **mainProgram**

    | Key                 | Value                                                      |
    | ------------------- | ---------------------------------------------------------- |
    | *key*               | *"mainProgram"* — defines which OpenSees binary to run     |
    | *value*             | Default: *"OpenSees"*                                      |
    | *inputMode*         | *"REQUIRED"*                                               |
    | *notes.enum_values* | Options include *OpenSees*, *OpenSeesSP*, and *OpenSeesMP* |
    
    → Although this app is called *OpenSees-express*, it seems the template allows flexibility to run other OpenSees binaries as well (if present in the container).
:::
      
:::{dropdown} **tclScript**

    | Key               | Value                                                    |
    | ----------------- | -------------------------------------------------------- |
    | *key*             | *"tclScript"* — the specific *.tcl* script to run        |
    | *value*           | Empty by default — user must provide a script name       |
    | *inputMode*       | *"REQUIRED"*                                             |
    | *notes.inputType* | *"fileInput"* — this gets linked to uploaded input files |
:::

### jobAttributes.parameterSet.archiveFilter
Controls what gets archived (i.e., saved after job completion):
:::{dropdown} Archive Filter
| Field                | Purpose                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------- |
| *includes*           | Empty — archive everything by default                                                       |
| *excludes*           | *"opensees-express.zip"*, *"tapisjob.env"* — avoids cluttering the archive with setup files |
| *includeLaunchFiles* | *true* — includes wrapper script and job manifest (for reproducibility)                     |
:::
  
###  jobAttributes.fileInputs

The app expects a **directory of inputs**:
:::{dropdown} Input Directory
| Field                 | Description                                                         |
| --------------------- | ------------------------------------------------------------------- |
| *name*                | *"Input Directory"* — shown in the UI                               |
| *inputMode*           | *"REQUIRED"* — user must supply this folder                         |
| *envKey*              | *"inputDirectory"* — used in the wrapper script                     |
| *notes.selectionMode* | *"directory"* — user selects a full directory, not individual files |
:::



## jobAttributes.notes
:::{dropdown} UI Metadata
These values are passed to the UI web form in DesignSafe.

| Field                          | Description                                          |
| ------------------------------ | ---------------------------------------------------- |
| *label*                        | *"OpenSees-EXPRESS (VM)"* — shown in the UI          |
| *helpUrl*                      | Link to user documentation                           |
| *hideNodeCountAndCoresPerNode* | *true* — simplifies UI for single-core apps          |
| *isInteractive*                | *false* — not an interactive app                     |
| *icon*                         | *"OpenSees"* — graphical icon used in the portal     |
| *category*                     | *"Simulation"* — categorizes the app on the platform |
:::


##  Summary

This *app.json* makes *OpenSees-express*:

* A **single-node, single-script app**
* Designed to **run inside a ZIP-based Docker container**
* Configured for **portable, containerized execution** on a small VM or cloud system
* Easy to use: users just upload a folder with a *.tcl* file and specify which file to run



