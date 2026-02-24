# Run a Tapis App
***Two Views of the Same Process (User Workflow + Tapis Runtime)***


A Tapis job submission has **one lifecycle**, but it can be described from two perspectives:

## A. What the app-user does (the “front” process)
::::{card} 
**User-facing workflow**: what you choose and what you provide (Portal / CLI / Tapipy)


:::{dropdown} **Install Tapipy**

Run this once to install the SDK:

```bash
pip install tapipy
```

tapipy may have already been installed in Jupyter Hub.
:::

:::{dropdown} **Connect to Tapis**

Create the client and log in:

```python
from tapipy.tapis import Tapis

# Replace with your credentials
t = Tapis(
    base_url="https://tacc.tapis.io",
    username="your-username",
    password="your-password",
    account_type="tacc"
)

t.get_tokens()  # Log in to Tapis
```

**Tip:** You only need to call *get_tokens()* once per session.

:::


:::{dropdown} **1) Choose an app (and version)**

You specify an `appId` and **version** (e.g., `opensees-mp-s3` or `...-latest`).
This determines:

* the input schema (what files/params are allowed)
* the runtime style (ZIP vs container)
* the wrapper entrypoint (what actually runs on the cluster)

:::

:::{dropdown} **2) Provide inputs and parameters**
Supply input files/directories and any runtime parameters defined by the app schema.

You provide:

* **file inputs** (files/dirs that must be staged to the execution system)
* **parameters** (simple values like flags, paths, numeric settings)
* optional **environment variables** (modules, pip installs, custom toggles)
* Archive system ID (e.g. *"tacc-archive"*)
* Where you want your outputs to be stored (*archivePath*)

  
:::

:::{dropdown} **3) Define execution settings (job attributes)**

You request compute resources:

* nodes, tasks/cores, walltime, queue/partition
* optional scheduler extras (reservation, constraints)

:::

:::{dropdown} **4) Submit Job**

Tapis submits the job to the execution system and tracks status.

* **Example Submission** using Tapipy

    ```python
    job = t.jobs.submitJob(
        jobName="my-first-job",
        appId="hello-world-1.0",
        parameters={},      # Replace with actual app parameters if needed
        fileInputs=[],      # Or provide input files here
        archiveSystemId="tacc-archive",
        archivePath="myuser/outputs/hello-job",
        archiveOnAppError=True
    )
    
    print("Job submitted!")
    print("Job ID:", job.id)
    print("Status:", job.status)
    ```


:::

:::{dropdown} **5) Monitor execution**
You track status from:

* Portal, CLI, or API/Tapipy
* logs produced by Slurm (stdout/stderr) and by your wrapper script (summary logs)


You can check on your job:

```python
job = t.jobs.getJob(jobUUID=job.id)
print("Current Status:", job.status)
```

Or just the status field directly:

```python
status = t.jobs.getJobStatus(jobUUID=job.id)
print(status.status)
```
* **Job Status Values (for Filtering)**

    Common values you can use for the *status* field:
    
    * *PENDING*
    * *STAGING_INPUTS*
    * *RUNNING*
    * *FINISHED*
    * *FAILED*
    * *CANCELLED*
    * *PAUSED*
    * *BLOCKED*

You can filter jobs by status like:

```python
jobs = client.jobs.listJobs(status='FINISHED')
```

Or via search:

```python
search_query = json.dumps({"status": "FAILED"})
jobs = client.jobs.listJobs(search=search_query)
```


:::

:::{dropdown} **6) Retrieve outputs**

When complete, outputs are available in the archive location and via the Files service for browsing/downloading/reuse.

* Outputs are archived to the configured archive system/path.
* You can browse, download, and reuse results in later workflows.

* **List available files**

```python
files = t.jobs.getJobOutputList(jobUUID=job.id)
for f in files:
    print(f.name, f.length)
```

* **Download a file:

```python
output = t.jobs.getJobOutputDownload(
    jobUUID=job.id,
    path="stdout.txt"
)

with open("stdout.txt", "wb") as f:
    f.write(output)
```

The file paths (like *"stdout.txt"*) depend on how your app writes output.


:::


:::{dropdown} Full Example Script
**Submit → poll → list outputs**

```python
from tapipy.tapis import Tapis
import json

t = Tapis(
    base_url="https://tacc.tapis.io",
    username="your-username",
    password="your-password",
    account_type="tacc"
)
t.get_tokens()

job = t.jobs.submitJob(
    jobName="my-first-job",
    appId="hello-world-1.0",
    # parameterSet / fileInputs structure can vary by app definition
    parameters={},
    fileInputs=[],
    archiveSystemId="tacc-archive",
    archivePath="myuser/outputs/hello-job",
    archiveOnAppError=True
)

print("Job ID:", job.id)
print("Status:", job.status)

# Poll status
job2 = t.jobs.getJob(jobUUID=job.id)
print("Current Status:", job2.status)

# Filter jobs (example)
search_query = json.dumps({"status": "FAILED"})
failed_jobs = t.jobs.listJobs(search=search_query)
print("Failed jobs returned:", len(failed_jobs))
```
:::

::::

## B. What Tapis does (the “internal” runtime process)
::::{card} 
**Runtime workflow**: what Tapis automates on the execution system (SSH + filesystem + scheduler + archiving)

The internal runtime workflow (stage → submit → run → archive)

This is the same lifecycle, described by the system actions that occur after you submit.

This section describes what happens after you click “Run Job” (or submit via API). The exact details vary by execution system and runtime type, but the pattern is consistent:

validate → stage → unpack/prepare → submit → monitor → archive


:::{dropdown} **1) Job Definition: Validation + job record creation**
A Tapis App is defined by:

* app.json → inputs, parameters, environment, runtime type
* tapisjob_app.sh → wrapper script executed on the HPC system
* optional supporting files (profiles, modules, docs)

When you submit a job, Tapis:
1. Validates your request against app.json
* required inputs present
* parameter types correct
* enums/schema constraints satisfied
* strictFileInputs enforced (if enabled)
2. Creates a **job UUID** and stores the resolved configuration (effective values)

Only after validation does the job move into staging.

:::

:::{dropdown} **2) Staging inputs (file-transfer phase #1)**

Tapis prepares the execution environment on the HPC system:

1. Creates a job working directory (location depends on the Execution System definition)
2. Stages your input directory/files into the job’s working directory
3. Stages the runtime asset (ZIP bundle or container image reference)
4. Applies permissions and writes internal metadata for tracking
No execution occurs in staging — this phase is file preparation.

:::

:::{dropdown} **3) Runtime preparation (ZIP unpack / container plan)**

A. **ZIP runtime**

* Tapis copies the ZIP into the job directory
* Extracts it in place
* Makes tapisjob_app.sh executable

In a ZIP runtime, the extracted bundle is effectively your “app container” — just implemented as a portable archive.

B. **Container runtime (Singularity/Apptainer)**

* Tapis ensures the image is available on the system
* Plans bind mounts (exec/input/output paths)
* Encodes the container command into the scheduler script

Tapis itself does not “run the container”; the scheduler-run script does.

:::

:::{dropdown} **4) Scheduler submission**

Tapis generates a batch script (e.g., Slurm), injects your resource requests and runtime command, then runs `sbatch`.
Tapis stores the scheduler job ID so it can poll state.

Tapis constructs a scheduler submission script using:
* queue/partition
* node/task/core counts
* time limits
* scheduler options (reservations, constraints)
* execution-system profile settings

Then it submits the batch job (e.g., via sbatch) and stores the scheduler job ID for monitoring.



:::

:::{dropdown} **5) Wrapper script execution (your code runs here)**

This is where the app logic lives.

Tha app's tapisjob_app.sh typically:
1. Initializes timers and logs
1. Loads modules (from defaults and/or user-provided lists)
1. Configures Python (optionally installs packages)
1. Chooses a launcher
* MPI → ibrun / srun
* serial → direct execution
1. Runs the main executable
* OpenSeesMP, OpenSeesSP, OpenSees, python3, etc.
1. Writes summary logs and exits with a code that Tapis can capture

Tapis does not interfere with what happens inside the wrapper — it only observes job state and outputs.


The app's wrapper script (e.g., `tapisjob_app.sh`) controls:

* module loads
* python environment / pip installs
* serial vs MPI launchers (`ibrun`, `srun`, etc.)
* what gets written to output/logs
* cleanup

Tapis does not “reach into” your runtime logic—it’s hands-off once Slurm is running your script.

:::

:::{dropdown} **6) Archiving outputs (file-transfer phase #2)**
After the app's wrapper exits:
1. Tapis creates the archive directory on the archive system/path
1. Copies outputs (excluding anything filtered by archiveFilter)
1. Includes Slurm logs (stdout/stderr) and wrapper logs
1. If archiveOnAppError=true, it still archives even when the job fails

This archiving phase can be slow if the output contains many small files.

:::

:::{dropdown} **7) Completion and user visibility**
Once archived, you can:
* browse outputs in the portal or via the Files API
* download logs and results
* compare runs across job UUIDs
* rerun with modified parameters
* share results with collaborators (where supported)

This completes the Tapis lifecycle:
stage → prepare → run → archive
:::


::::

The key idea is that Tapis is an **orchestrator**: it **stages files**, **generates a scheduler script**, **submits to Slurm**, **monitors**, then **archives** outputs.

## The lifecycle at a glance (swimlane)
:::{card} 

```
USER (Portal / CLI / Tapipy)              TAPIS (Jobs Service + Files)                 HPC (Stampede3 / Slurm)
───────────────────────────────────       ─────────────────────────────────────────   ─────────────────────────
1) Pick app + version  ───────────────▶   Validate request (app schema) 
2) Provide inputs/params ─────────────▶   Create job record (UUID, config)
3) Request resources ─────────────────▶   Stage inputs + runtime (file transfer)
                                          Build batch script
                                          sbatch batch_script ─────────────────────▶  Queue (PENDING)
                                          Poll scheduler status  ◀──────────────────  Run (RUNNING)
4) Monitor status  ◀───────────────────   Map scheduler states to Tapis states
5) Get results  ◀──────────────────────   Archive outputs (file transfer)
                                          Provide outputs via Files API
```
:::


> On shared systems like **Stampede3**, jobs may queue before running due to demand — this delay is the trade-off for accessing powerful resources.



## Appendix: Tapis job execution (SSH + Slurm timeline)
:::{card} ***A “shell view” of what the Jobs service typically does***

Tapis does **not** run jobs internally. The Jobs service automates what you would otherwise do manually on an HPC system:

1. SSH into the execution system (as the effective HPC user)
1. Create job directories
1. Stage inputs and runtime assets
1. Write a scheduler batch script
1. Submit and monitor the scheduler job
1. Archive outputs and expose them via the Files service

**Condensed behind-the-scenes timeline**

    SSH → mkdir job directories
    SSH + Files → stage inputs
    SSH → copy/unpack ZIP (or locate container image)
    SSH → write scheduler script
    SSH → submit (sbatch)
    SSH → poll (squeue / sacct)
    SSH → collect output metadata
    Files Service → deliver outputs

:::

## Where to look when debugging

::::{card} 

If stuck in STAGING_INPUTS → input transfers, too many files, remote source delays

If stuck in QUEUED/PENDING → scheduler wait time (partition, allocation, walltime)

If failing in RUNNING → wrapper logic, module loads, env vars, executable errors

If slow after FINISHED → archiving overhead (again: too many files)




:::{card}
**Important performance note**: many “slow jobs” are not slow because compute is slow — they’re slow because file transfer is slow. The **input staging** and **output archiving** phases can dominate runtime when there are many small files. When possible: reduce file counts, reuse common datasets from Work/Scratch, or bundle inputs/outputs as a ZIP/TAR that you unpack/pack inside your wrapper.
:::

---


**Practical debugging: “Where is my time going?”**
***Use the lifecycle to localize bottlenecks***



When users say “Tapis is slow,” it usually means one of these stages:

* **Slow before RUNNING** → input staging or queue wait
* **Slow after FINISHED** → archiving (lots of files or large directories)
* **Slow during RUNNING** → your executable/runtime environment

**File-transfer advice (high impact):**

* Minimize *file count* (thousands of small files is worse than one big file)
* Keep common datasets (e.g., ground motions) in **Work/Scratch**, and reuse them
* Bundle inputs/outputs as **ZIP/TAR** and extract/pack inside the wrapper
* Consider writing intermediate results to Work/Scratch and collecting only what you need at the end

::::
