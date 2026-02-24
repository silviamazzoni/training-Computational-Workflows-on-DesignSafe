# Compute-Environment Guide
***Making the Right Choice***

Selecting the right environment — **where your analysis is run** — is essential for balancing speed, scale, and control:

* Choose **JupyterHub** for:

  * Interactive analysis: Developing and testing scripts interactively (Tcl or Python)
  * Rapid prototyping: Running OpenSees, OpenSeesMP, or OpenSeesSP with test-scale jobs
  * Visualizing results
  * Automating workflows
  * Using either Tcl/python scripts or Jupyter notebooks
  * Small to medium computations
  * Immediate feedback with minimal setup

* Use the **OpenSees-Express VM** for:

  * Running Tcl-based scripts with **no queue**
  * Getting started with OpenSees without SLURM or command-line setup
  * Quick jobs that don’t require MPI or long runtime

* Move to **HPC Environment** when:

  * You need large-scale, long run time, or parallel computations
  * Your memory or CPU demands exceed per-container limits
  * You’re ready to scale up or automate large parameter sweeps


## Feature Comparison

| Feature                 | JupyterHub (Kubernetes)                            | OpenSees-Express VM                   | HPC Environment                            |
| ----------------------- | -------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------ |
| **Access Mode**         | Interactive browser-based workspace                | Form-based web interface, backend VM          | Web Portal, SLURM, or command line                   |
| **Supported Versions**  | OpenSees (Tcl), OpenSeesMP, OpenSeesSP, OpenSeesPy | OpenSees (sequential Tcl only)                | OpenSees (Tcl), OpenSeesMP, OpenSeesSP, OpenSeesPy |
| **Resource Allocation** | One node, 8 cores / 20 GB RAM per session           | Shared VM (\~2–4 cores, \~8–16 GB RAM)        | Multi-core/multi-node with SLURM,  high-memory options depending on system and request                       |
| **Scheduling / Queue**  | Instant start (until max capacity reached)         | Immediate execution — no queue                | **Queued** execution based on priority, resource request, and availability via SLURM, or Jupyter for HPC                             |
| **Interactivity**       | Full (terminal + notebooks)                        | No GUI — backend VM only                      | Non-interactive batch mode + interactive                             |
| **Isolation**           | Container CPU/RAM are dedicated, but physical nodes are shared<sup>1</sup>    | Shared VM across jobs                         | Dedicated job resources per submission                 |
| **Use Case**            | Development, automation, testing | Quick Tcl-only jobs, entry point to HPC usage | Large-scale, long-duration, MPI jobs                   |
| **Ease of Use**         | High — notebooks, terminals, Python & Tcl support  | Very high — simple form-based submittal       | Medium — requires SLURM scripts or tuning job settings |
| **Best For**            | Testing, prototyping, post-processing, scripting   | Getting started with OpenSees (Tcl)           | Production workflows, OpenSeesMP/SP batch studies      |

<sup>1</sup> *Note: JupyterHub gives you exclusive access to container resources (CPU and memory), but the physical node may host other users' containers, which can lead to minor I/O contention during heavy disk activity.*

## Choosing the Optimal Compute Environment

| Environment                | Access Method                | Resources & Scaling                     | Best For                                               |
| -------------------------- | ---------------------------- | --------------------------------------- | ------------------------------------------------------ |
| **JupyterHub**             | Browser (notebooks/terminal) | Up to 8 cores / 20 GB RAM per container | Prototyping, OpenSeesPy, quick test loops, automation            |
| **OpenSees-Express VM**    | Web Portal (form-based)      | Shared lightweight VM                   | Tcl scripts, small serial jobs, easiest point of entry |
| **HPC Environment** | SSH + SLURM (Tapis)            | Full system access, massive scale                  | Parallel OpenSees jobs, large simulations, production  |


## Choosing Your Compute Path

Here’s a simple **decision tree** to guide you:

* **Are you new to OpenSees and want an easy way to run a sequential Tcl job?**
  → Use **OpenSees-Express** (no CLI or SLURM knowledge needed)
  
* **Are you developing, testing, or interactively exploring?**
  → Use **JupyterHub** for full interactivity and flexibility


* **Does your job fit within <8 cores and <20 GB RAM?**
  → Yes → Continue using **JupyterHub**

* **Otherwise:**
  → Switch to **HPC batch jobs**:

  * Write a SLURM script
  * Submit it to the scheduler
  * Wait in queue and retrieve results from HPC file systems

