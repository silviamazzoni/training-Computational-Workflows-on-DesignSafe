# Accessing HPC

***How to Use TACC's HPC on DesignSafe***

High Performance Computing (HPC) systems like **Stampede3** at TACC are powerful clusters built for large-scale simulations and data analysis. Unlike personal computers, you don’t run programs directly — instead, you interact with a **layered environment** designed to manage thousands of users fairly and efficiently.

This section explains the architecture of HPC systems, your access options (via **JupyterHub**, **SSH**, or **Tapis**), and how jobs are submitted and executed.

---

## HPC Architecture: Components and Roles

| Component           | Purpose                                                                    |
| ------------------- | -------------------------------------------------------------------------- |
| **Login Nodes**     | Where users connect via SSH or JupyterHub to prepare and submit jobs       |
| **Compute Nodes**   | Where your jobs actually run (scheduled by SLURM)                          |
| **Storage Systems** | `/home`, `/work`, and `/scratch` for input, output, and intermediate files |

When you connect to TACC via SSH or JupyterHub, you're entering a **login node** — a shared environment for lightweight tasks like file editing, module loading, and job submission. Actual computation happens on **compute nodes**, which are allocated by the **SLURM scheduler** when you submit a job.

---

## Submitting Jobs: The Queueing Model

On HPC systems, you do **not** run scripts directly like on your desktop. Instead:

1. You write a **SLURM job script** specifying resources and commands.
2. Submit it using `sbatch job.slurm`.
3. SLURM places your job in a **queue**, schedules resources, and runs it.
4. The job runs independently without real-time input — like launching a rocket.

> Think of it like checking a bag at the airport: you hand it off, and the system handles the rest.

---

## Interactive Options

* ### idev: Temporary Shell on Compute Node

    To get a real shell on a compute node for compiling, testing, or debugging:
    
    ```bash
    idev -N 1 -n 4 -p development -t 00:30:00
    ```
    
    This launches an **interactive SLURM job**, granting temporary access to a compute node where you can:
    
    * Test MPI/OpenMP configurations
    * Debug scripts and workflows
    * Run small-scale exploratory jobs

---

## JupyterHub: Web-Based Interactive Access

TACC’s **JupyterHub** (e.g., TAP) and DesignSafe’s **JupyterLab HPC environments** both provide browser-based interfaces to HPC, but with important distinctions.

* ### TACC JupyterHub (TAP)

    * Submits your Jupyter session as a **job** that runs on a container or virtual node
    * You get access to full resources (e.g., 8 cores, 20 GB RAM)
    * Sessions may queue before launching due to resource limits

* ### DesignSafe JupyterLab HPC (CPU/GPU)

    * Offers **dedicated access to Stampede3 compute nodes**
    * Originally intended for machine learning workflows, now widely used for:
    
      * OpenSees
      * Python simulations
      * Other research code needing HPC scale
    * Comes in multiple flavors (CPU, GPU, Native), and may evolve
    
    Despite being interactive, both systems are still subject to HPC constraints like **queueing**, **resource limits**, and **node availability**.

---

## The HPC Environment via SSH

For full control and flexibility:

1. **SSH to the login node**
2. Prepare scripts, stage files, and manage your data
3. Submit jobs with SLURM manually

This approach is ideal for:

* Complex configurations
* Advanced Linux workflows
* Fine-grained resource requests

Even in this mode, you can still leverage **Tapis** to automate file transfers, script generation, and job submission.

---

## Integrating with Tapis

Whether you use Jupyter, SSH, or the Web Portal, Tapis allows you to:

* Upload/download files
* Generate SLURM job scripts
* Submit jobs programmatically
* Retrieve output automatically

This is especially useful for **parametric studies**, **automated campaigns**, and **reproducible workflows**.

---

## Summary: HPC Access Model

| Method                    | Best For                                                              |
| ------------------------- | --------------------------------------------------------------------- |
| **Login Node (SSH)**      | Setup, editing, compiling, staging data                               |
| **Compute Node (SLURM)**  | Actual execution of simulations                                       |
| **idev**                  | Real-time debugging and test runs on compute nodes                    |
| **JupyterHub (TACC)**     | Interactive sessions via queued containerized jobs                    |
| **DesignSafe JupyterLab** | Full-node interactive access for OpenSees, ML, and Python workflows   |
| **Tapis Automation**      | Orchestrating multi-job pipelines and managing files programmatically |

Understanding this model explains why:

* Jobs don’t start instantly — they’re **queued**
* You can’t “just run” a script from your terminal — you must **submit**
* Jupyter sessions are powerful but also **resource-limited**
* All methods, whether batch or interactive, follow the **same SLURM-backed model**

