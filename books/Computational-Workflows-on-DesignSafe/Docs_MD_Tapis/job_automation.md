# Scaling Jobs with Tapis
***Moving beyond interactive job submission***

At some point, the Web Portal, interactive environments like JupyterHub, or even scripts run on your own computer, stop being the best tool—not because they are limited, but because **your workflow has grown**.

These are excellent for development, testing, and small-to-moderate runs, but they are not designed to manage large numbers of long-running, resource-intensive jobs.

You may be ready to:

* run **many jobs** (parameter studies, ensembles, UQ, sensitivity analyses)
* increase **model size and runtime**
* eliminate repetitive clicking and manual bookkeeping
* build **repeatable, scriptable workflows** that you can rerun, share, and extend


This is the point where you move beyond purely interactive execution—whether from the Web Portal, JupyterHub, or your local machine—and begin using **Tapis as an automation layer** to reliably launch, monitor, and manage jobs on HPC systems.

---

## You now have two complementary paths:

### 1. Write your own SLURM scripts

This path gives you direct, low-level control over how jobs run on the scheduler.

* Start from **existing SLURM scripts** used inside Tapis apps.
* Customize nodes, cores, MPI layout, job arrays, and I/O strategies.
* Chain jobs manually using dependencies or wrapper scripts.
* Best suited for users who want the scheduler itself to be part of the workflow logic.

**Best for:** large MPI jobs, job arrays, tightly managed scratch workflows, advanced scheduler usage.

---

### 2. Automate jobs using Tapis

This path focuses on **workflow automation**, while letting Tapis handle the HPC details.

#### Step 1 — Use existing Tapis apps programmatically

Your first step is *not* to write new apps.

Instead, you:

* reuse **existing, production-tested Tapis apps** (e.g., OpenSeesMP, OpenSeesSP, OpenSeesPy)
* submit jobs via **Tapipy (Python)** or **tapis-cli**
* pass inputs and parameters programmatically
* launch many jobs with structured variations (loops, tables, JSON configs)

At this stage, you are using the **exact same execution environment** as the Web Portal — just without the clicking.

#### Step 2 — Build automation around those apps

Once programmatic submission is in place, you can:

* generate inputs automatically
* track job IDs and states
* link pre-processing and post-processing steps
* re-run failed cases or extend studies incrementally

This is often where Jupyter becomes a **workflow controller**, not the execution environment.

#### Step 3 — Write your own Tapis apps (when needed)

Only after the above do you typically need to:

* create a new app wrapper
* define a new input schema
* support a custom executable or workflow pattern

By then, you already understand:

* what the app needs to expose
* how users will automate it
* how it fits into larger pipelines

---

## Why this matters for scientific workflows

Using Tapis apps as **reusable templates** is a cornerstone of scalable research computing.

They:

* enforce consistent input/output handling
* reduce user error and environment drift
* enable the same workflow to run from the Web Portal, Jupyter, or scripts
* make collaboration and reproducibility practical

Most importantly, this approach lets researchers **scale their science without rebuilding infrastructure each time**.

