#  Tapis-App Types

Tapis Apps provide a reproducible, portable way to run scientific workflows on DesignSafe’s HPC systems. Each app defines **what to run**, **how to run it**, and **what environment it runs in**, while Tapis handles staging, execution, monitoring, and output collection. This section summarizes the core concepts so users understand how an app translates into a running job on systems such as **Stampede3**, **Frontera**, and **Jetstream2**.

---

##  1. What a Tapis App Describes

A Tapis App is a JSON specification that declares:

1. **Runtime type**

   * How the application environment is provided (ZIP, Singularity/Apptainer, or Docker).
2. **Execution mode**

   * Whether the job runs through a scheduler (BATCH) or directly on the host (FORK).
3. **Command and arguments**

   * The executable or script to run once the environment is ready.
4. **Inputs, parameters, and outputs**

   * File staging, primitive parameters, directory handling, and result collection.

The App does *not* run anything by itself—it defines the template for future **Jobs**.

---

##  2. The App–System–Job Relationship

Tapis execution involves three layers:

1. **App (what to run)**

   * Specifies runtime, executable path, input schema, environment variables, etc.

1. **Execution System (where it runs)**

   Defines:

   * Login protocol (SSH), scheduler (Slurm), and queue options
   * Filesystem locations for input/output/exec
   * Which runtime technologies are allowed (ZIP, Singularity)
   
   * **DesignSafe/TACC systems allow ZIP and Singularity, not Docker.**

1. **Job (an instance of the app)**

   * User-provided input values → staged into the execution directory → launched under the system’s scheduler or host environment.

---

##  3. Runtime Types: How App Environments Are Provided

Tapis supports three runtime types.
On DesignSafe HPC, **ZIP** and **SINGULARITY** are the standard choices.

---

:::{dropdown} **A. ZIP Runtime (Lightweight, Module-Based)**

The app’s `containerImage` is a `.zip`/`.tar` archive containing scripts, templates, and wrapper files.
At job start:

1. The archive is copied into the job’s execution directory.
2. It is unpacked.
3. The designated executable is run **directly on the host**, using the system’s modules (e.g., `module load hdf5`, `module load opensees`, MPI).

**Best for:**

* Apps that rely on **TACC modules**
* OpenSees/OpenSeesPy workflows
* Rapid iteration without building containers
* Simple driver scripts, Tcl/Python wrappers

**Why DesignSafe uses this heavily:**
It is fast, simple, and leverages HPC-optimized software already provided by TACC.

:::

:::{dropdown} **B. SINGULARITY / APPTAINER Runtime (Reproducible, Self-Contained)**

Singularity (now **Apptainer**) is the HPC container engine used on all TACC clusters.

The app’s `containerImage` refers to a `.sif` file containing a complete software environment.
At runtime, Tapis does something similar to:

```bash
apptainer run myapp.sif [args]
```

All inputs and outputs are bound into the container, and your executable runs inside a fully reproducible user-space environment.

**Best for:**

* Custom scientific environments
* Conda-based workflows
* Applications not available as TACC modules
* Cross-cluster portability (Jetstream2 ↔ Stampede3 ↔ local)
* Stable, version-locked pipelines

**Why use it:**
If your app needs a specific OS, Python stack, compiler, or third-party library, Singularity gives you full control.

:::

:::{dropdown} **C. DOCKER Runtime (Cloud and VM Use Only)**

Docker images are supported **only** when the execution system allows Docker.
HPC compute nodes at TACC **do not** support Docker, so this runtime is not used on DesignSafe systems.

Use Docker only for apps running on VMs (e.g., Jetstream2) where the system explicitly declares Docker support.
:::

---

##  4. Execution Model: BATCH vs FORK Jobs

:::{dropdown} **A. BATCH Jobs**

* Submitted to the system scheduler (Slurm for TACC)
* Support multi-node jobs
* Required for MPI/OpenSeesMPI/OpenSeesMP
* Outputs collected after completion

Most HPC workloads—including all OpenSeesMP apps—use **BATCH**.

:::

:::{dropdown} **B. FORK Jobs**

**FORK jobs** are a different execution model and are *not* typical for HPC clusters.

FORK jobs:
* Run directly on the login/exec host without a scheduler
* Single-node, short, lightweight tasks
* Good for quick utilities or file preprocessing
  
Tapis also supports **FORK jobs**, which are fundamentally different:

* No scheduler (no SLURM, no PBS)
* No queueing
* No resource allocation
* Tapis executes *tapisjob.sh* **directly on the target host**

This is appropriate for:

* Small utility servers
* Virtual Machines (VMs)
* Lightweight services
* Systems without a batch scheduler

⚠️ On large HPC systems like Stampede3:

* FORK jobs are **not used**
* All compute work must go through SLURM
* Batch jobs are mandatory to enforce fair usage and resource limits

DesignSafe apps typically avoid FORK except for trivial tools.
:::

---

##  5. Input Staging & Shared Filesystems

Regardless of runtime type, Tapis stages all inputs into a **single job directory** on a shared filesystem (e.g., `/scratch`, `/work2`).
Because TACC systems use shared parallel filesystems:

* Every compute node can see the same staged files
* Inputs are **not copied separately** to each node
* Multi-node jobs simply access the same directory

This is crucial for MPI and OpenSeesMP workflows.

---

##  6. Job Launch Flow (What Actually Happens)

A Tapis job on DesignSafe follows this flow:

1. **User submits job request** with parameter values and input file references.
2. Tapis **creates the job directory** (`execSystemExecDir`) on Stampede3.
3. **Input files are staged** into that directory.
4. The App’s runtime is applied:

   * ZIP → archive unpacked
   * Singularity → `.sif` mounted and evaluated
5. Tapis constructs a **launch script** (Slurm batch script for BATCH jobs).
6. The job is **submitted through Slurm**.
7. The job runs on compute nodes.
8. Output files are collected into `execSystemOutputDir`.
9. Tapis returns job status and output metadata.

This model is consistent across all Tapis-supported DesignSafe HPC apps.

---

##  7. When to Use Each Runtime (Simple Rule of Thumb)

| Use Case                                      | Best Runtime                                                                     |
| --------------------------------------------- | -------------------------------------------------------------------------------- |
| Relying on TACC modules (OpenSees, HDF5, MPI) | **ZIP**                                                                          |
| Need reproducibility across clusters          | **SINGULARITY**                                                                  |
| Custom Python/Conda environments              | **SINGULARITY**                                                                  |
| Fast development & simple scripts             | **ZIP**                                                                          |
| VM-based workflows with Docker available      | **DOCKER**                                                                       |
| OpenSeesMP / multi-node jobs                  | **ZIP** or **SINGULARITY** (both work; ZIP is simpler if modules are sufficient) |

---

##  8. Summary

Tapis Apps give researchers a structured, repeatable way to run scientific software on DesignSafe’s HPC resources.
Choosing between **ZIP** and **SINGULARITY** depends on whether you want to:

* **Leverage TACC’s optimized environment** → ZIP
* **Package your own environment** → Singularity / Apptainer

Understanding runtimes, execution systems, and input staging allows users to design robust, scalable workflows that integrate smoothly with Stampede3, Frontera, and Jetstream2.
