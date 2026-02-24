# app.json Schema
These tables describe the schema for the Tapis Applications.
You can learn more in the apps definition in the following:
* (Tapis Apps Documentation)[https://tapis.readthedocs.io/en/latest/technical/apps.html]
* (Tapis Jobs Documentation)[https://tapis.readthedocs.io/en/latest/technical/jobs.html]

:::{dropdown} **Sample Schema**: opensees-mp-s3 app.json
```
  sharedAppCtx: "wma_prtl"
  isPublic: True
  tenant: "designsafe"
  id: "opensees-mp-s3"
  version: "latest"
  description: "Runs all the processors in parallel. Requires understanding of parallel processing and the capabilities to write parallel scripts."
  owner: "wma_prtl"
  enabled: True
  versionEnabled: True
  locked: False
  runtime: "ZIP"
  runtimeVersion: None
  runtimeOptions: None
  containerImage: "tapis://cloud.data/corral/tacc/aci/CEP/applications/v3/opensees/latest/OpenSees/opensees.zip"
  jobType: "BATCH"
  maxJobs: 2147483647
  maxJobsPerUser: 2147483647
  strictFileInputs: True
  uuid: "1410a584-0c5e-4e47-b3b0-3a7bea0e1187"
  deleted: False
  created: "2025-02-20T18:01:49.005183Z"
  updated: "2025-07-25T19:55:59.261049Z"
  sharedWithUsers: []
  tags: ["portalName: DesignSafe", "portalName: CEP"]
  jobAttributes: {
    description: None
    dynamicExecSystem: False
    execSystemConstraints: None
    execSystemId: "stampede3"
    execSystemExecDir: "${JobWorkingDir}"
    execSystemInputDir: "${JobWorkingDir}"
    execSystemOutputDir: "${JobWorkingDir}"
    dtnSystemInputDir: "!tapis_not_set"
    dtnSystemOutputDir: "!tapis_not_set"
    execSystemLogicalQueue: "skx"
    archiveSystemId: "stampede3"
    archiveSystemDir: "HOST_EVAL($WORK)/tapis-jobs-archive/${JobCreateDate}/${JobName}-${JobUUID}"
    archiveOnAppError: True
    isMpi: False
    mpiCmd: None
    cmdPrefix: None
    nodeCount: 2
    coresPerNode: 48
    memoryMB: 192000
    maxMinutes: 120
    fileInputs: [
      {
        name: "Input Directory"
        description: "Input directory that includes the tcl script as well as any other required files. Example input is in tapis://designsafe.storage.community/app_examples/opensees/OpenSeesMP"
        inputMode: "REQUIRED"
        autoMountLocal: True
        envKey: "inputDirectory"
        sourceUrl: None
        targetPath: "inputDirectory"
        notes: {
          selectionMode: "directory"
        }
      }
    ]
    fileInputArrays: []
    subscriptions: []
    tags: []
    parameterSet: {
      appArgs: [
        {
          arg: "OpenSeesMP"
          name: "mainProgram"
          description: None
          inputMode: "FIXED"
          notes: {
            isHidden: True
          }
        }
        {
          arg: None
          name: "Main Script"
          description: "The filename only of the OpenSees TCL script to execute. This file should reside in the Input Directory specified. To use with test input, use 'freeFieldEffective.tcl'"
          inputMode: "REQUIRED"
          notes: {
            inputType: "fileInput"
          }
        }
      ]
      containerArgs: []
      schedulerOptions: [
        {
          arg: "--tapis-profile OpenSees_default"
          name: "OpenSees TACC Scheduler Profile"
          description: "Scheduler profile for the default version of OpenSees"
          inputMode: "FIXED"
          notes: {
            isHidden: True
          }
        }
      ]
      envVariables: []
      archiveFilter: {
        includeLaunchFiles: True
        includes: []
        excludes: []
      }
      logConfig: {
        stdoutFilename: ""
        stderrFilename: ""
      }
    }
  }
  notes: {
    icon: "OpenSees"
    label: "OpenSeesMP"
    helpUrl: "https://www.designsafe-ci.org/user-guide/tools/simulation/#opensees-user-guide"
    category: "Simulation"
    isInteractive: False
    hideNodeCountAndCoresPerNode: False
  }

```
:::

The following tables provide details on the different components of an app's schema.

::::::{dropdown} **Application Attributes**

:::{dropdown} **All Attributes**
| Attribute        | Type          | Example               | Notes                                                                                                              |
| ---------------- | ------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------ |
| tenant           | String        | designsafe            | Name of the tenant for which the application is defined.<br>* `tenant + version + id` must be unique.                   |
| id               | String        | my-ds-app             | Name of the application. URI safe. <br>* tenant + $version* + id must be unique. <br>* Allowed characters: Alphanumeric \[0-9a-zA-Z], \[-.\_\~].<br>* **Required at creation.** |
| version          | String        | 0.0.1                 | Version of the application. URI safe. <br>* tenant + $version* + id must be unique. <br>* Allowed characters: Alphanumeric \[0-9a-zA-Z], \[-.\_\~].<br>* **Required at creation.**                                                        |
| description      | String        | A sample application  | Optional description                                                                                               |
| owner            | String        | jdoe                  | Username of the owner. Default is `${apiUserId}`                                                                   |
| enabled          | boolean       | FALSE                 | Whether app is enabled. Default is TRUE.                                                                           |
| versionEnabled   | boolean       | FALSE                 | Whether version is enabled. Default is TRUE.                                                                       |
| locked           | boolean       | FALSE                 | Indicates if version is currently locked. Locking disallows updates. Default is FALSE.                             |
| runtime          | enum          | SINGULARITY           | Runtime to be used when executing the application. <br>* Runtime: DOCKER, SINGULARITY, ZIP. <br>* Default is DOCKER.           |
| runtimeVersion   | String        | 2.5.2                 | Optional version or range of versions.                                                                             |
| runtimeOptions   | \[enum]       |                       | Options that apply to specific runtimes. <br>* Options: NONE, SINGULARITY\_RUN. <br>* Default is NONE. <br>* WARNING Please note that use of SINGULARITY_START is no longer supported.                                  |
| containerImage   | String        | docker.io/hello-world | Reference for the container image. <br>* Other examples: <br>* Singularity: shub://GodloveD/lolcow, <br>* Docker: tapis/hello-tapis:0.0.1<br>* **Required at creation.**                     |
| jobType          | enum          | BATCH                 | Default job type: BATCH, FORK. <br>* Jobs will be of this type by default. <br>* May be overridden in the job submit request.<br>* Default is FORK.                                   |
| maxJobs          | int           | 10                    | Max number of jobs that can be running for this app on a system.<br>* System may also limit the number of jobs. <br>* Set to -1 for unlimited. <br>* Default is unlimited.                                                                               |
| maxJobsPerUser   | int           | 2                     | Max number of jobs per job owner.<br>* System may also limit the number of jobs.<br>* Set to -1 for unlimited.<br>* Default is unlimited.     |
| strictFileInputs | boolean       | FALSE                 | TRUE disallows unnamed file inputs. <br>* Indicates if a job request is allowed to have unnamed file inputs.<br>* If TRUE then a job request may only use named file inputs defined in the app.<br>* Default is FALSE.                                                              |
| **jobAttributes**    | JobAttributes |                       | Attributes related to job execution. See below.                                                                    |
| tags             | \[String]     |                       | List of tags as simple strings.                                                                                    |
| notes            | String        | {"project": "myproj"} | Simple metadata in the form of a Json object.Not used by Tapis.                                             |
| uuid             | UUID          | 20281                 | Auto-generated by service.                                                                                               |
| created          | Timestamp     | 2020-06-19T15:10:43Z  | When the app was created. Maintained by service.                                 |
| updated          | Timestamp     | 2020-07-04T23:21:22Z  | When the app was last updated. Maintained by service.                                                    |
:::

:::::{dropdown} ***jobAttributes***

:::{dropdown} **All Attributes**
| Attribute              | Type              | Example                    | Notes                               |
| ---------------------- | ----------------- | -------------------------- | ----------------------------------- |
| description            | String            |                            | * Description to be filled in when this application is used to run a job. <br>* Macros allow this to act as a template to be filled in at job runtime. |
| execSystemId           | String            |                            | * Specific system on which the application is to be run.    |
| execSystemExecDir      | String            | \${JobWorkingDir}/jobs/... | * Application's working directory. * Directory where application assets are staged. <br>* Current working directory at application launch time. <br>* Macro template variables such as ${JobWorkingDir} may be used. <br>* Default is ${JobWorkingDir}/jobs/${JobUUID}     |
| execSystemInputDir     | String            | \${JobWorkingDir}/jobs/... | * Directory where Tapis is to stage the inputs required by the application. <br>* Macro template variables such as ${JobWorkingDir} may be used. <br>* Default is ${JobWorkingDir}/jobs/${JobUUID}        |
| execSystemOutputDir    | String            | \${JobWorkingDir}/jobs/... | * Directory where Tapis expects the application to store its final output results. <br>* Files here are candidates for archiving. <br>* Macro template variables such as ${JobWorkingDir} may be used. <br>* Default is ${JobWorkingDir}/jobs/${JobUUID}/output         |
| dtnSystemInputDir      | String            |                            | * Directory relative to DTN rootDir to which input files will be transferred. <br>* Transfer happens prior to launching the application. <br>* Can be overriden by job submission request. <br>* Optional. If set will trigger use of DTN. <br>* Default is !tapis_not_set         |
| dtnSystemOutputDir     | String            |                            | * Directory relative to DTN rootDir from which output files will be transferred. <br>* Transfer happens during archiving phase of job execution. <br>* Can be overriden by job submission request. <br>* Optional. If set will trigger use of DTN. <br>* Default is !tapis_not_set      |
| execSystemLogicalQueue | String            | normal                     | * Queue name                          |
| archiveSystemId        | String            |                            | * System to use when archiving outputs.                   |
| archiveSystemDir       | String            | \${JobWorkingDir}/jobs/... | * Directory on archiveSystemId where outputs will be placed. <br>* This will be relative to the effective root directory defined for archiveSystemId. <br>* Default is ${JobWorkingDir}/jobs/${JobUUID}      |
| archiveOnAppError      | boolean           | TRUE                       | * Indicates if outputs should be archived if there is an error while running job. <br>* The default is TRUE.          |
| isMpi                  | boolean           | FALSE                      | * Indicates that application is to be executed as an MPI job. <br>* The default is FALSE.                  |
| mpiCmd                 | String            | mpirun, ibrun -n 4         | * Command used to launch MPI jobs. <br>* Prepended to the command used to execute the application. <br>* Conflicts with cmdPrefix if isMpi is set.                |
| cmdPrefix              | String            |                            | * String prepended to the application invocation command. <br>* Conflicts with mpiCmd if isMpi is set.           |
| **fileInputs**             | \[FileInput]      |                            |* Collection of file inputs that must be staged for the application. <br>* Each input must have a name. <br>* strictFileInputs =TRUE means only inputs defined here may be specified for job. <br>* See table below.                   |
| **fileInputArrays**        | \[FileInputArray] |                            | * Collection of arrays of inputs that must be staged for the application. <br>* Each input must have a name. All inputs in an array have the same target directory. <br>* strictFileInputs =TRUE means only inputs defined here may be specified for job. <br>* See table below.                  |
| **parameterSet**           | ParameterSet      |                            | * Various collections used during job execution. <br>* App arguments, container arguments, scheduler options, environment variables, etc. CLI args, env, filters. See below.  |
| nodeCount              | int               |                            | * Number of nodes to request during job submission.                  |
| coresPerNode           | int               |                            | * Number of cores per node to request during job submission.               |
| memoryMB               | int               |                            | * Memory in megabytes to request during job submission.                |
| maxMinutes             | int               |                            | * Run time to request during job submission.               |
| subscriptions          |                   |                            | * Notification subscriptions. <br>* See table below.         |
| tags                   | \[String]         |                            | * List of tags as simple strings.                                |
:::

::::{dropdown} ***fileInput* Attributes**

| Attribute      | Type    | Notes                                         |
| -------------- | ------- | --------------------------------------------- |
| name           | String  | Identifying label associated with the input. Typically used during a job request.<br>* **Required at creation time.**                           |
| description    | String  | Optionaldescription.                        |
| inputMode      | enum    | Indicates how input is to be treated when processing individual job requests.<br>* REQUIRED, OPTIONAL, FIXED<br>* Default is OPTIONAL.|
| autoMountLocal | boolean | Indicates if Jobs service should automatically mount file paths into containers.<br>* Note that not all container runtimes require this.<br>* Setting to FALSE allows user complete control using containerArg parameters.<br>* Default is TRUE.  |
| sourceUrl      | String  | Source used by Jobs service when staging file inputs.                              |
| targetPath     | String  | Target path used by Jobs service when staging file inputs.                          |

::::


::::{dropdown} ***fileInputArray* Attributes**

| Attribute   | Type      | Notes                                         |
| ----------- | --------- | --------------------------------------------- |
| name        | String    | Identifying label associated with the input. Typically used during a job request.<br>* **Required at creation time.**                            |
| description | String    | Optional description.                          |
| inputMode   | enum      | REQUIRED, OPTIONAL, FIXED<br>* Default is OPTIONAL. |
| sourceUrls  | \[String] | Array of sources used by Jobs service when staging file inputs.                   |
| targetDir   | String    | Target directory used by Jobs service when staging file inputs.       |

::::

::::{dropdown} ***parameterSet* Attributes**

:::{dropdown} **All Attributes**
| Attribute        | Type            | Notes                             |
| ---------------- | --------------- | --------------------------------- |
| **appArgs**          | \[Arg]          | Command line arguments passed to the application.<br>* See table below for more information on Arg type entries.<br>* For more information on appArgs please see the chapter on Jobs         |
| **containerArgs**    | \[Arg]          | Command line arguments passed to the container runtime.<br>* See table below for more information on Arg type entries.<br>* For more information on containerArgs please see the chapter on Jobs     |
| **schedulerOptions** | \[Arg]          | Scheduler options passed to the HPC batch scheduler.<br>* See table below for more information on Arg type entries.<br>* For more information on schedulerOptions please see the chapter on Jobs |
| **envVariables**     | \[KeyValuePair] | Environment variables placed into the runtime environment.<br>* Each entry has key (required) and value (optional) as well as other attributes.<br>* See table KeyValuePair Attributes below for more information.<br>* For more information on envVariables please see the chapter on Jobs             |
| **archiveFilter**    | ArchiveFilter   | Sets of files to include or exclude when archiving.<br>* Default is to include all files in execSystemOutputDir.<br>* See table below for details of ArchiveFilter structure.<br>* For more information on archiveFilter support please see the chapter on Jobs            |
:::

:::{dropdown} ***appArgs* Attributes**

| Attribute   | Type   | Example              | Notes                                                             |
| ----------- | ------ | -------------------- | ----------------------------------------------------------------- |
| name        | String |                      | Identifying label associated with the argument.<br>* **Required at creation time.**                                           |
| description | String |                      | Optional description of the argument which may include usage, purpose, etc.                                            |
| inputMode   | enum   |                      | Indicates how argument is to be treated when processing individual job requests.<br>* Modes: REQUIRED, FIXED, INCLUDE_ON_DEMAND, INCLUDE_BY_DEFAULT<br>* Default is INCLUDE_ON_DEMAND.<br>* REQUIRED: Must be provided in a job request.<br>* FIXED: Completely defined in the application and not overridable in a job request.<br>* INCLUDE_ON_DEMAND: Included if referenced in a job request.<br>* INCLUDE_BY_DEFAULT: Included unless include=false in a job request. |
| arg         | String |                      | Value for the argument<br>* Required at creation time.                         |
| notes       | String | {"fieldType": "int"} | Optional Metadata in the form of a Json object, such as type, allowed values, etc.<br>* Not used by Tapis.                    |

:::

:::{dropdown} ***containerArgs* Attributes**
:::

:::{dropdown} ***schedulerOptions* Attributes**
from: (Tapis Jobs Documentation)[https://tapis.readthedocs.io/en/latest/technical/jobs.html]

Specify HPC batch scheduler arguments for the container runtime using the schedulerOptions parameter. Arguments specified in the application definition are appended to those in the submission request. The arguments for each scheduler are passed using that scheduler’s conventions.

Tapis defines a special scheduler option, --tapis-profile, to support local scheduler conventions. Data centers sometimes customize their schedulers or restrict how those schedulers can be used. The Systems service manages SchedulerProfile resources that are separate from any system definition, but can be referenced from system definitions. The Jobs service uses directives contained in profiles to tailor application execution to local requirements.

As an example, below is the JSON input used to create the TACC scheduler profile.

The moduleLoads array contains one or more objects. Each object contains a moduleLoadCommand, which specifies the local command used to load each of the modules (in order) in its modulesToLoad list.

The hiddenOptions array identifies scheduler options that the local implementation prohibits. Options specified here will have the corresponding Slurm option suppressed. Supported options are “MEM” for --mem and “PARTITION” for --partition. Including an option in the array indicates that the corresponding Slurm option should never be passed through to Slurm.

```
{
    "name": "TACC",
    "owner": "user1",
    "description": "Test profile for TACC Slurm",
    "moduleLoads": [
        {
            "moduleLoadCommand": "module load",
            "modulesToLoad": ["tacc-singularity"]
        }
    ],
    "hiddenOptions": ["MEM"]
}
```

Scheduler-Specific Processing: Jobs will perform macro-substitution on Slurm scheduler options --job-name or -J. This substitution allows Slurm job names to be dynamically generated before submitting them.

:::


::::{dropdown} ***envVariables* (KeyValuePair) Attributes**

Specify key-value pairs that will be injected as environment variables into the application’s container when it is launched. Key-value pairs specified in the execution system definition, application definition, and job submission request are aggregated using precedence ordering (system < app < request) to resolve conflicts.

Both the key and value are required, though the value can be an empty string. Descriptions are optional but if present must contain 1 or more characters.

| Attribute   | Type   | Example         | Notes           |
| ----------- | ------ | --------------- | --------------- |
| key         | String | INPUT\_FILE     | Environment variable name. Required. |
| value       | String | /tmp/file.input | Environment variable value           |
| description | String |                 | Optional Description       |
| inputMode   | enum   | REQUIRED        | As in Arg table<br>* Indicates how argument is to be treated when processing individual job requests.<br>* Modes: REQUIRED, FIXED, INCLUDE_ON_DEMAND, INCLUDE_BY_DEFAULT<br>* Default is INCLUDE_BY_DEFAULT.<br>* REQUIRED: Must be provided in a job request or application definition.<br>* FIXED: Not overridable in application or job request.<br>* INCLUDE_ON_DEMAND: Included if referenced in a job request.<br>* INCLUDE_BY_DEFAULT: Included unless include=false in a job request.|
| notes       | String | {}              | Simple metadata in the form of a Json object.<br>* Not used by Tapis.   |






::::

:::{dropdown} ***archiveFilter* Attributes**

The archiveFilter conforms to this JSON schema:
```
"archiveFilter": {
   "type": "object",
   "properties": {
      "includes": {"type": "array", "items": {"type": "string", "minLength": 1}, "uniqueItems": true},
      "excludes": {"type": "array", "items": {"type": "string", "minLength": 1}, "uniqueItems": true},
      "includeLaunchFiles": {"type": "boolean"}
   },
   "additionalProperties": false
}
```

An archiveFilter can be specified in the application definition and/or the job submission request. The includes and excludes arrays are merged by appending entries from the application definition to those in the submission request.

The excludes filter is applied first, so it takes precedence over includes. If excludes is empty, then no output file or directory will be explicitly excluded from archiving. If includes is empty, then all files in execSystemOutputDir will be archived unless explicitly excluded. If includes is not empty, then only files and directories that match an entry and not explicitly excluded will be archived.

Each includes and excludes entry is a string, a string with wildcards or a regular expression. Entries represent directories or files. The wildcard semantics are that of glob (*), which is commonly used on the command line. Tapis implements Java glob semantics. To filter using a regular expression, construct the pattern using Java regex semantics and then preface it with REGEX: (case sensitive). Here are examples of globs and regular expressions that could appear in a filter:

```
"myfile.*"
"*2021-*-events.log"
"REGEX:^[\\p{IsAlphabetic}\\p{IsDigit}_\\.\\-]+$"
"REGEX:\\s+"
```

When includeLaunchFiles is true (the default), then the script (tapisjob.sh) and environment (tapisjob.env) files that Tapis generates in the execSystemExecDir are also archived. These launch files provide valuable information about how a job was configured and launched, so archiving them can help with debugging and improve reproducibility. Since these files may contain application secrets, such database passwords or other credentials, care must be taken to not expose private data through archiving.

If no filtering is specified at all, then all files in execSystemOutputDir and the launch files are archived.


| Attribute          | Type      | Notes                                                 |
| ------------------ | --------- | ----------------------------------------------------- |
| includes           | \[String] | Files to include when archiving after execution of the application.<br>* excludes list has precedence.                                      |
| excludes           | \[String] | Files to skip when archiving after execution of the application.<br>* excludes list has precedence.                   |
| includeLaunchFiles | boolean   | Indicates if Tapis generated launch scripts are to be included when archiving.

The default is TRUE. |

:::

:::{dropdown} ***logConfig* Spec**
A LogConfig can be supplied in the job submission request and/or in the application definition, with the former overriding the latter when both are supplied. In supported runtimes (currently Singularity and ZIP), the logConfig parameter can be used to redirect the application container’s stdout and stderr to user-specified files.

:::

:::{dropdown} **MPI and Related Support**

On many systems, running Message Passing Interface (MPI) jobs is simply a matter of launching programs that have been configured or compiled with the proper MPI libraries. Most of the work in employing MPI involves parallelizing program logic and specifying the correct libraries for the target execution system. Once that is done, a command such as mpirun (or on TACC systems, ibrun) is passed the program’s pathname and arguments to kick off parallel execution.

Tapis’s mpiCmd parameter lets users set the MPI launch command in a system definition, application definition and/or job submission request (lowest to highest priority). For example, if mpiCmd=mpirun, then the string “mpirun ” will be prepended to the command normally used to execute the application. Some MPI launchers have their own parameters, for instance, mpiCmd=ibrun -n 4 requests 4 MPI tasks.

The isMpi parameter is specified in an application definition and/or job request to toggle MPI launching on or off. This switch allows the same system to run both MPI and non-MPI jobs depending on the needs of particular jobs or applications. The isMpi default is false, so this switch must be explicitly turned on to run an MPI job. When turned on, isMpi requires cmdMpi be assigned in the system, application and/or job request.

The cmdPrefix parameter provides generalized support for launchers and is available in application definitions and job submission requests. Like mpiCmd, a cmdPrefix value is simply prepended to a program’s pathname and arguments. Being more general, cmdPrefix could specify an MPI launcher, but it’s not supported in system definitions and does not have a toggle to control usage.

mpiCmd and cmdPrefix are mutually exclusive; so if isMpi is true, then cmdPrefix must not be set.

:::


::::


:::::



::::::

### inputMode
Applications use their AppArgSpecs to pass default values to job requests. 

The AppArgSpec’s inputMode determines how to handle arguments during job processing. An inputMode field can have these values:

* **REQUIRED**
The argument must be provided for the job to run. If an arg value is not specified in the application definition, then it must be specified in the job request. When provided in both, the job request arg value overrides the one in application.

* **FIXED**
The argument is completely defined in the application and not overridable in a job request.

* **INCLUDE_ON_DEMAND**
The argument, if complete, will only be included in the final argument list constructed by Jobs if it’s explicitly referenced and included in the Job request. This is the default value.

* **INCLUDE_BY_DEFAULT**
The argument, if complete, will automatically be included in the final argument list constructed by Jobs unless explicitly excluded in the Job request.

