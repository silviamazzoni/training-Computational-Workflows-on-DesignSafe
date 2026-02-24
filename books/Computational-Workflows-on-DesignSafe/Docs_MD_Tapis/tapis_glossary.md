# Tapis-App Glossary
**Glossary for New Tapis-App Users**

This Glossary is Focused on DesignSafe + Stampede3 workflows

    
* **App**
    
    A JSON definition describing *what to run*, *how to run it*, and *what runtime environment is required*. It is a template for creating Jobs.
    
    
* **Job**
    
    An execution instance of an App with specified input files, parameters, and runtime arguments.
    A Job runs on the designated **Execution System**.
    
    
* **Execution System**
    
    A Tapis-defined HPC or VM environment that runs jobs.
    Defines:
    
    * Scheduler (Slurm for TACC HPC)
    * Login method (SSH)
    * Filesystem paths (*execDir*, *inputDir*, *outputDir*)
    * Allowed runtimes (ZIP, Singularity)
    * Default modules (if applicable)
    
    
* **runtime**
    
    Specifies how the application environment is provided:
    
    * **ZIP** — Unpacked scripts/binaries run in host environment
    * **SINGULARITY** — Run inside a *.sif* container image
    * **DOCKER** — Only supported on systems that allow Docker (not TACC HPC)
    
    Example:
    ```json
    "runtime": "ZIP"
    ```
    
* **containerImage**
    
    The source of the app’s runtime environment:
    
    * Path or URL to *.zip*/*.tgz* archive (ZIP runtime)
    * Path to *.sif* image (Singularity runtime)
    * Docker image reference (if DOCKER runtime allowed)
    
    Example (ZIP):
    ```json
    "containerImage": "tapis://designsafe.storage/apps/opensees-sp.zip"
    ```
    
    
* **jobType**
    
    Defines how the job is launched:
    
    * **BATCH**
    
      * Submitted through Slurm
      * Supports multi-node jobs
      * Used for OpenSeesSP/MP and most HPC workflows
    
    * **FORK**
    
      * Runs directly on host without scheduler
      * Single-node, lightweight tasks
    
    Example:
    ```json
    "jobType": "BATCH"
    ```
    
    
* **execSystemExecDir**
    
    Directory on the execution system where:
    
    * ZIP archives are unpacked
    * Singularity images may be copied
    * The job’s Slurm launch script is placed
    * The actual execution happens
    
    Essentially: **the working directory for the running job**.
    
    
* **execSystemInputDir**
    
    Directory where Tapis stages all job inputs.
    This is a **shared filesystem** on TACC, so all compute nodes can read the same staged files.
    
    
* **execSystemOutputDir**
    
    Directory where job output files are placed after completion.
    Tapis transfers files from here to the Job record’s “outputs” listing.
    
    
* **Input Staging**
    
    The process by which Tapis:
    
    1. Creates job directory on the execution system
    2. Copies all referenced input files into it
    3. Ensures shared visibility across compute nodes
    
    On TACC HPC, input staging goes to the same shared storage visible from all nodes.
    
    
* **Parameter**
    
    A primitive value passed into the app:
    
    * Numbers
    * Strings
    * Flags
    * Options
    
    Used for command-line arguments, filenames, counts, etc.
    
    
* **ArgString**
    
    The final command that Tapis constructs using:
    
    * Executable
    * Parameters
    * Input references
    
    Example:
    ```
    OpenSeesMP model.tcl -n 48 -param 3.2
    ```
    
    
* **Scheduler Options**
    
    Additional Slurm settings:
    
    * Queue/partition
    * Number of nodes
    * Cores per node
    * Wall time
    
    These can be specified in the App and sometimes overridden in the Job.
    
    
* **Apptainer / Singularity**
    
    HPC container runtime used on TACC systems:
    
    * Unprivileged (safe for multi-user clusters)
    * Executes *.sif* images
    * Binds host directories into container
    
    Used for reproducible, environment-controlled apps.
    
    
* **Modules (TACC Environment Modules**
    
    System-provided software components that can be loaded at runtime:
    ```
    module load hdf5
    module load opensees
    module load python
    ```
    ZIP runtime apps rely heavily on modules.
    
    
* **Shared Filesystem**
    
    Parallel filesystem (e.g., */work2*, */scratch*) visible from all compute nodes.
    Ensures that multi-node jobs can access the same staged inputs without replication.
    
