# App Structure
***Understanding the OpenSeesMP Tapis App Structure***

The OpenSeesMP Tapis app is defined by three key files that work together to describe how the application runs on TACC’s Stampede3 system. These files control everything from the user-facing interface to the backend execution behavior. Understanding the role of each file is essential if you plan to modify the app, develop your own, or debug its behavior.

## The three core files are:

* **app.json** – Describes the app metadata and user inputs. This is the *public interface* of the app — it tells Tapis (and DesignSafe) how to collect inputs and how to represent the app in the web portal or API.

* **profile.json** – Defines the *execution environment*. It specifies which modules to load, which HPC system to use, and what runtime settings should be applied when the job runs.

* **tapisjob_app.sh** – The *runtime script*. This Bash script is what actually gets executed on the compute node. It launches the OpenSeesMP executable using the inputs and environment defined in the other two files.

Together, these three files allow the OpenSeesMP app to:

* Validate user input,
* Launch jobs on Stampede3 with the correct software environment, and
* Execute OpenSeesMP in a repeatable, scalable, and performance-optimized way.


```{dropdown} app.json: Defining the HPC App for Stampede3

The *app.json* file declares the app’s behavior to the Tapis platform. It sets the app up as a **ZIP-based batch job** (not containerized) and defines how input files are passed, which scripts to run, how many resources to allocate, and how results are archived.

* **Highlights**

    | Field                     | Description and Defaults                                                   |
    |--------------------------|-----------------------------------------------------------------------------|
    | *executionSystemId*      | *"stampede3"* — targets the TACC Stampede3 HPC system                       |
    | *jobType*                | *"BATCH"* — uses SLURM queues                                               |
    | *runtime*                | *"ZIP"* — runs from unpacked directory with no container                    |
    | *execSystemLogicalQueue*| *"skx"* — assigns the job to the Skylake queue                              |
    | *nodeCount*              | 2 nodes, each with 48 cores (96 total)                                      |
    | *memoryMB*               | 192,000 MB (192 GB) total memory allocation                                 |
    | *mainProgram*            | *"OpenSeesMP"* — the parallel OpenSees executable (fixed argument)          |
    | *Input Directory*        | Directory provided by the user, must include the *.tcl* script and data     |
    | *Main Script*            | File name of the *.tcl* script to run (filename only, no path)              |



* **User Must Provide**:

    | Name             | Description                                                              |
    |------------------|--------------------------------------------------------------------------|
    | Input Directory  | A full directory containing the *.tcl* script and any supporting files   |
    | Main Script      | Just the filename (e.g., *model.tcl*) — must match a file in the input dir |
    
    The app enforces *strictFileInputs: true*, so filenames must be exact, and all required data must be inside the provided directory.

* **Output and Archiving**

    Results (including SLURM output/error logs and OpenSees output files) are archived to:
    
    \$WORK/tapis-jobs-archive/\${JobCreateDate}/\${JobName}-\${JobUUID}
    
    
    This allows reproducibility and remote access to job results.

```




````{dropdown} profile.json: Configuring the Runtime Environment

The *profile.json* defines which software modules must be loaded on Stampede3 **before execution**. This ensures that *OpenSeesMP* and its dependencies are available in the runtime environment.

* **Modules Loaded**

    | Module           | Purpose                                  |
    |------------------|------------------------------------------|
    | *hdf5/1.14.4*     | Enables HDF5 support (optional but useful) |
    | *opensees*        | Loads the default OpenSees build (includes OpenSeesMP) |
    
    These modules are loaded using the standard TACC command:
    
    module load hdf5/1.14.4 opensees
    
    
    No containerization is used — the app runs **natively** on Stampede3 compute nodes.

````



:::{dropdown} tapisjob_app.sh: Running the MPI Job via SLURM

This *tapisjob_app.sh* script is the job’s actual execution wrapper. It runs on the compute node(s) after the job is scheduled, and uses *ibrun* to launch OpenSeesMP in parallel across the requested cores.

* **Runtime Behavior

```
set -x

BINARYNAME=$1         # Typically "OpenSeesMP"
INPUTSCRIPT=$2        # Filename like "model.tcl"

# Strip directory from input script
TCLSCRIPT="${INPUTSCRIPT##*/}"

cd "${inputDirectory}"  # Navigate to user-provided input folder

# Launch in parallel using TACC's SLURM wrapper
ibrun $BINARYNAME $TCLSCRIPT

```

**Notes**

* *ibrun* handles distribution of the process across nodes/cores
* *inputDirectory* is set automatically by Tapis from user inputs
* *$1* and *$2* come from the *parameterSet.appArgs* defined in *app.json*

If OpenSees exits with an error, the script will print the failure and terminate early.

**Example Job Behavior**

Given:

* Input Directory: *tapis://.../OpenSeesMP*
* Main Script: *freeFieldEffective.tcl*

The app will:

1. Load the OpenSees and HDF5 modules
2. Move into the input directory
3. Run:
ibrun OpenSeesMP freeFieldEffective.tcl

across 96 cores (2 nodes × 48 cores).

:::


