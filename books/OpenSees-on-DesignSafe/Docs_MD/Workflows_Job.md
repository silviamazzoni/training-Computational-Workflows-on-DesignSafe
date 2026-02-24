# Job Workflow
***Where and How Your Jobs Run***

Once you understand the underlying architecture, the next step is choosing the most efficient path for your work. The tables below summarize the options in terms of interfaces, APIs, execution locations, and best-fit scenarios for OpenSees on DesignSafe.

---

## Choosing Your Workflow

The tables below break down **where your jobs run**, **how you can submit them**, and **which option to pick** for different scenarios. They’re designed to be a quick reference so you can jump straight to the workflow that best fits your analysis.

### 1. Job Interfaces and Execution Environments
**The available interfaces, where the job runs, and typical use cases.**

This table shows each available interface, whether it uses Tapis, where the job runs, and typical use cases.

| Interface Method                          | Uses Tapis?            | Execution Location                               | Description / Use Case                                                      | Recommended for OpenSees? |
| ----------------------------------------- | ---------------------- | ------------------------------------------------ | --------------------------------------------------------------------------- | ------------------------- |
| **JupyterHub (Kubernetes Cluster)**       | ✅ Yes                  | Kubernetes container at TACC                     | Interactive development, testing, small to mid-scale jobs (up to 8 cores).  | ✅ Yes                     |
| **Submit to HPC via Tapis in Jupyter**    | ✅ Yes                  | HPC systems via Tapis or Tapis Apps              | Use Tapipy or CLI to launch parameter studies or automate workflows.        | ✅ Yes                     |
| **Submit to VM (e.g., OpenSees-EXPRESS)** | ✅ Yes                  | Dedicated single-node VM via Tapis or Tapis Apps | Tapis-only access; queue-free sequential job submission.                    | ✅ Yes (sequential only)   |
| **Web Portal**                            | ✅ Yes (via Tapis Apps) | VM (OpenSees-EXPRESS) or HPC nodes               | Submit Tcl-based OpenSees jobs via preconfigured forms and apps.            | ✅ Yes (Tcl only)          |
| **SSH (Terminal Access)**                 | ❌ Optional             | TACC HPC systems (Stampede3, etc.)               | Direct manual scripting, SLURM submission, and full environment control.    | ✅ Yes (all types)         |
| **Jupyter on HPC Node**                   | ❌ No                   | Single compute node on Vista, Frontera           | JupyterLab session on a compute node (queued); not configured for OpenSees. | ❌ No                      |



### 2. Job Submission Options
***How* you send work to the compute environment.**

This table focuses on how you send work to the compute environment, whether that’s through an interactive session, a portal, or a batch system.

| Submission Method                          | Description                                                                                    | Uses Tapis?                   |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------- | ----------------------------- |
| **Run directly in JupyterHub**             | Execute short jobs in your live Jupyter container (up to 8 CPUs, 20 GB RAM).                   | ❌ No                          |
| **Submit using Tapis Apps (Web Portal)**   | Launch preconfigured jobs (e.g., OpenSeesMP) using forms. Handles SLURM and output management. | ✅ Yes                         |
| **Submit using Tapis Apps (from Jupyter)**   | Use Python (`tapipy`) or CLI tools to submit jobs to Stampede3, etc., directly from notebooks. Launch preconfigured jobs (e.g., OpenSeesMP) using prebuilt Tapis wrappers. Handles SLURM and output management. | ✅ Yes                         |
| **Submit to HPC via Tapis (from Jupyter)** | Use Python (`tapipy`) or CLI tools to submit jobs to Stampede3, etc., directly from notebooks. Write your own custom job wrappers for Tapis. Handles SLURM and output management.| ✅ Yes                         |
| **Manual SLURM submission (via SSH or JupyterHub on HPC)**      | Login to HPC systems, write and submit batch scripts manually.                                 | ❌ No (unless wrapped by user) |


### 3. Summary Comparison
**Side-by-side comparison of major access methods**

This table provides a side-by-side comparison of major access methods, their environments, best uses, and OpenSees compatibility.

| Category               | JupyterHub                     | Web Portal          | SSH + CLI                     | Jupyter on HPC                          |
| ---------------------- | ------------------------------ | ------------------- | ----------------------------- | --------------------------------------- |
| **Interface**          | Jupyter notebooks, terminal    | Web browser         | Terminal (SSH)                | Jupyter notebooks, terminal             |
| **Exec Environment**   | Kubernetes container (8 cores) | HPC or dedicated VM | HPC systems (Stampede3, etc.) | HPC systems (Stampede3, etc.)           |
| **Submission Options** | Run locally or submit jobs via Tapis       | Tapis apps          | SLURM batch (manual)          | Run locally, via Tapis, or manual SLURM |
| **Best for**           | All       | Standard batch jobs | Advanced/custom workflows     | Specilty jobs                              |
| **OpenSeesPy Support** | ✅ Yes                          | ❌ No                | ✅ Yes                         | ✅ Yes                                   |



---



## Quick Decision Guide

*Use this quick reference to choose your path, then see the tables below for details.*

* **Are you developing, testing, or exploring interactively?**
  → Use **JupyterHub**.

* **Is your workload small (<8 cores, <20 GB RAM)?**
  → Still use **JupyterHub**.

* **Do you need larger or production-scale runs?**
  → Submit an **HPC batch job**.

  * Just a few jobs?
    → Use the **Web Portal**.

  * Running many jobs or parameter sweeps?
    → Use **Tapis inside JupyterHub** for scalable automation.


