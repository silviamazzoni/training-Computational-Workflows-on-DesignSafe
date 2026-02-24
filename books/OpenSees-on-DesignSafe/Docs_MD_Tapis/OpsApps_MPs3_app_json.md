# app.json
    
This file declares the app to the Tapis system. It defines how the app runs, what files and parameters it expects, what system it runs on, and how results are stored.

##  App-Definition File
:::{dropdown} **app.json**
The following json was copied from github and may have changed.
```
{
  "id": "opensees-mp-s3",
  "version": "latest",
  "description": "Runs all the processors in parallel. Requires understanding of parallel processing and the capabilities to write parallel scripts.",
  "owner": "${apiUserId}",
  "enabled": true,
  "runtime": "ZIP",
  "runtimeVersion": null,
  "runtimeOptions": null,
  "containerImage": "tapis://cloud.data/corral/tacc/aci/CEP/applications/v3/opensees/latest/OpenSees/opensees.zip",
  "jobType": "BATCH",
  "maxJobs": -1,
  "maxJobsPerUser": -1,
  "strictFileInputs": true,
  "jobAttributes": {
    "execSystemConstraints": null,
    "execSystemId": "stampede3",
    "execSystemExecDir": "${JobWorkingDir}",
    "execSystemInputDir": "${JobWorkingDir}",
    "execSystemOutputDir": "${JobWorkingDir}",
    "execSystemLogicalQueue": "skx",
    "archiveSystemId": "stampede3",
    "archiveSystemDir": "HOST_EVAL($WORK)/tapis-jobs-archive/${JobCreateDate}/${JobName}-${JobUUID}",
    "archiveOnAppError": true,
    "isMpi": false,
    "mpiCmd": null,
    "parameterSet": {
      "appArgs": [
        {
          "name": "mainProgram",
          "arg": "OpenSeesMP",
          "inputMode": "FIXED",
          "notes": {
            "isHidden": true
          }
        },
        {
          "name": "Main Script",
          "description": "The filename only of the OpenSees TCL script to execute. This file should reside in the Input Directory specified. To use with test input, use 'freeFieldEffective.tcl'",
          "arg": null,
          "inputMode": "REQUIRED",
          "notes": {
            "inputType": "fileInput"
          }
        }
      ],
      "containerArgs": [],
      "schedulerOptions": [
          {
              "name": "OpenSees TACC Scheduler Profile",
              "description": "Scheduler profile for the default version of OpenSees",
              "inputMode": "FIXED",
              "arg": "--tapis-profile OpenSees_default",
              "notes": {
                  "isHidden": true
              }
          },
          {
              "name": "TACC Reservation",
              "description": "Reservation input string",
              "inputMode": "INCLUDE_ON_DEMAND",
              "arg": null,
              "notes": {
                  "isHidden": true
              }
          }
      ],
      "envVariables": [],
      "archiveFilter": {
        "includes": [],
        "excludes": [],
        "includeLaunchFiles": true
      }
    },
    "fileInputs": [
      {
        "name": "Input Directory",
        "inputMode": "REQUIRED",
        "sourceUrl": null,
        "targetPath": "inputDirectory",
        "envKey": "inputDirectory",
        "description": "Input directory that includes the tcl script as well as any other required files. Example input is in tapis://designsafe.storage.community/app_examples/opensees/OpenSeesMP",
        "notes": {
          "selectionMode": "directory"
        }
      }
    ],
    "fileInputArrays": [],
    "nodeCount": 2,
    "coresPerNode": 48,
    "memoryMB": 192000,
    "maxMinutes": 120,
    "subscriptions": [],
    "tags": []
  },
  "tags": [
    "portalName: DesignSafe",
    "portalName: CEP"
  ],
  "notes": {
      "label": "OpenSeesMP",
      "helpUrl": "https://www.designsafe-ci.org/user-guide/tools/simulation/#opensees-user-guide",
      "hideNodeCountAndCoresPerNode": false,
      "isInteractive": false,
      "icon": "OpenSees",
      "category": "Simulation",
      "showReservation": true
  }
}
```
:::


## Key Fields Explained

| Field                        | Meaning                                                          |
| ---------------------------- | ---------------------------------------------------------------- |
| *id*                         | App identifier (*opensees-mp-s3*)                                |
| *runtime*                    | *"ZIP"* — unpacked file-based runtime (not a container)          |
| *jobType*                    | *"BATCH"* — submits to SLURM queue as a scheduled job            |
| *execSystemId*               | *"stampede3"* — the compute cluster where this app runs          |
| *execSystemLogicalQueue*     | *"skx"* — Stampede3 Skylake queue                                |
| *nodeCount* / *coresPerNode* | 2 nodes × 48 cores (default)                                     |
| *archiveSystemId*            | *"stampede3"* — output is saved back to user's *$WORK* directory |
| *isMpi*                      | *false* (handled manually using ibrun)                           |

## Inputs

| Input Name        | Description                                                               |
| ----------------- | ------------------------------------------------------------------------- |
| *Input Directory* | A **folder** containing all input files, including the main *.tcl* script |
| *Main Script*     | The filename of the *.tcl* script (e.g., *"model.tcl"*)                   |

## Parameters

```json
"appArgs": [
  {
    "name": "mainProgram",
    "arg": "OpenSeesMP",
    "inputMode": "FIXED"
  },
  {
    "name": "Main Script",
    "description": "...",
    "inputMode": "REQUIRED"
  }
]
```

* *mainProgram* = *"OpenSeesMP"* is fixed and passed as *$1* to the script
* *"Main Script"* = passed as *$2*, the filename to execute

## Output Archiving

Output files, including *.out*, *.err*, and simulation results, are archived to:

```
$WORK/tapis-jobs-archive/<date>/<jobname>-<uuid>/
```

This allows for future access and reproducibility.

