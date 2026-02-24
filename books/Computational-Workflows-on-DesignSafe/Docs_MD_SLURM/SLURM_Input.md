# Job Inputs
***SLURM Job Inputs and Job Scripts***

When running jobs on TACC HPC systems (such as **Stampede3**), all batch computations are controlled by **SLURM** (Simple Linux Utility for Resource Management). Whether you submit jobs through the DesignSafe portal, the TACC web portal, or directly from the command line, the underlying mechanism is the same: **a SLURM job script**.

This section explains:

* what a SLURM job script is,
* how job *inputs* are expressed through SLURM directives,
* why specific parameters are required, and
* how these parameters affect scheduling, execution, and data handling.

---

## What Is a SLURM Job Script?

A **SLURM job script** is a Bash script that serves two purposes at once:

1. **Resource request and job description**
   You declare *what you need* (nodes, cores, time, queue, allocation).

2. **Execution instructions**
   You define *what to run* once those resources are assigned (modules, executables, scripts).

SLURM reads the job script **before your job ever starts running**. Based on the declared parameters, it decides **when**, **where**, and **on how many resources** your job can run.

This separation is fundamental:

* SLURM scheduling decisions are made *before execution*
* Your application logic runs *after resources are allocated*

---

## Anatomy of a SLURM Job Script

All SLURM job scripts follow the same high-level structure:

```bash
#!/bin/bash
#SBATCH [resource and job directives]

# optional setup (modules, environment)
# optional diagnostics (echo SLURM variables)
# application execution
```

The key idea is that **everything beginning with `#SBATCH` is interpreted by SLURM**, not by Bash.

---

## Core Job Input Parameters (Required for All Jobs)

The following parameters appear at the **top of the script** and define the job’s resource footprint and lifecycle.

### Allocation (`-A`)

Specifies **which TACC allocation account** is charged for this job.

Why this exists:

* TACC resources are allocated through proposals or projects
* SLURM must know *which project pays* for the compute time

If the allocation is invalid or expired, the job will not start.

---

### Queue / Partition (`-p`)

Selects the **queue (partition)** where the job will run.

Why this exists:

* Different queues support different job sizes and runtimes
* Queues enforce policy limits (maximum nodes, time limits, priorities)

Choosing the smallest appropriate queue usually results in **faster scheduling**.

---

### Maximum Runtime (`-t`)

Sets the **wall-clock time limit** for the job.

Why this exists:

* SLURM schedules jobs by fitting them into available time windows
* Jobs that run longer than requested can block others

Important implications:

* Jobs exceeding this time are **terminated**
* File staging (input and output transfers) counts toward runtime
* Underestimating time may cause premature termination
* Overestimating time may increase queue wait

Formats may be system-specific (e.g. `HH:MM:SS` or minutes).

---

### Node Count (`-N`)

Requests the number of **compute nodes**.

Why nodes matter:

* A node is a full physical machine
* Memory, local disks, and network bandwidth are allocated per node
* MPI jobs scale across nodes, not just cores

Requesting more nodes than needed increases cost and queue time.

---

### Total Tasks / Cores (`-n`)

Specifies the **total number of processes (tasks)**.

Why SLURM separates nodes and tasks:

* Nodes define *hardware*
* Tasks define *parallel processes*

For MPI jobs:

```
total tasks = number of MPI ranks
```

For memory-heavy workloads, fewer tasks per node may be preferable.

---

### Job Name (`-J`)

A human-readable identifier for the job.

Why this matters:

* Appears in the queue (`squeue`)
* Used in output file naming
* Helps distinguish multiple similar jobs

Good job names significantly improve traceability.

---

### Output and Error Files (`-o`, `-e`)

Redirect standard output and error streams to files.

Why this matters:

* Keeps logs persistent after the job finishes
* Separating output and error simplifies debugging
* `%j` expands to the SLURM job ID, preventing overwrites

---

## Data Archiving and Output Location (DesignSafe Context)

When jobs are launched through DesignSafe/Tapis:

* Inputs are staged into a **job working directory** on a shared filesystem
* Outputs are automatically copied to an **archive system** after completion

### Archive System

Defines *where results are saved long-term* (typically MyData).

### Archive Directory

Defines *which folder* in the archive receives results.

Why defaults are recommended:

* DesignSafe organizes outputs by date and job name
* Automatic archiving avoids manual transfers
* Custom locations are useful only for advanced workflows

---

## Example: Complete SLURM Job Script (Stampede3)

```bash
#!/bin/bash
#----------------------------------------------------
# SLURM Job Script for Stampede3
#----------------------------------------------------
#SBATCH -A my_allocation
#SBATCH -J my_job_name
#SBATCH -o my_job_name.o%j
#SBATCH -e my_job_name.e%j
#SBATCH -N 2
#SBATCH -n 48
#SBATCH -p skx
#SBATCH -t 02:00:00

#----------------------------------------------------
# Load software environment
#----------------------------------------------------
module load hdf5
module load opensees

#----------------------------------------------------
# Optional diagnostics
#----------------------------------------------------
echo "Job ID: $SLURM_JOB_ID"
echo "Nodes: $SLURM_JOB_NODELIST"
echo "Total tasks: $SLURM_NTASKS"

#----------------------------------------------------
# Run application
#----------------------------------------------------
ibrun OpenSeesMP input.tcl
```

---

## Why SLURM Requires This Structure

SLURM job inputs may feel verbose, but they exist to solve real system-level problems:

| Design Choice                         | Reason                                        |
| ------------------------------------- | --------------------------------------------- |
| Explicit resource requests            | Enables fair sharing and efficient scheduling |
| Fixed runtime limits                  | Prevents runaway jobs                         |
| Separation of scheduling vs execution | Allows pre-planning and backfilling           |
| Node-based allocation                 | Matches physical hardware                     |
| Declarative inputs                    | Enables automation and reproducibility        |

Once understood, this structure becomes a strength: **the same job description can be scaled from a single test run to thousands of production runs with minimal changes**.

---

## Summary: Key Job Inputs at a Glance

| Parameter        | Purpose                   |
| ---------------- | ------------------------- |
| Allocation       | Who pays for the job      |
| Queue            | Where the job runs        |
| Runtime          | How long it may run       |
| Nodes            | How many machines         |
| Tasks            | How much parallelism      |
| Job Name         | Human-readable identifier |
| Output/Error     | Persistent logs           |
| Archive Settings | Long-term storage         |

---

If you’d like, next we can:

* add **MPI-specific patterns** (ranks, per-node files),
* explicitly contrast **manual SLURM vs Tapis-launched jobs**, or
* create a **minimal “mental model” diagram** tying scheduling, filesystems, and execution together.
