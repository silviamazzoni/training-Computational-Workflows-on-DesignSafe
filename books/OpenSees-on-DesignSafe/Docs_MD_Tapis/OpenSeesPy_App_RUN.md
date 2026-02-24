# Run DS OpenSeesPy App

***Notebook Demonstration Using the 'designsafe-openseespy-s3' App***

This Jupyter notebook demonstrates **how to submit, configure, and monitor batch OpenSeesPy jobs on DesignSafe** using the **'designsafe-openseespy-s3'** Tapis application.

Rather than focusing on OpenSeesPy modeling itself, the goal here is to help you understand the **job-submission workflow**:

* how your files are staged,
* how execution happens on Stampede3 under SLURM,
* how portal inputs map to runtime behavior, and
* how to diagnose and debug jobs after submission.

By the end of this notebook, you should feel comfortable adapting the same pattern to **your own OpenSeesPy scripts**, whether they are serial, MPI-enabled, or part of a small parameter study.

---

## What This Notebook Covers

This notebook walks through a **minimal but complete workflow** for running OpenSeesPy on DesignSafe:

* Preparing an **input directory** containing a Python script and supporting files
* Selecting appropriate **portal inputs** (script name, MPI flag, resources)
* Submitting a job programmatically from Jupyter
* Understanding how the app:

  * stages inputs,
  * loads modules,
  * installs Python packages,
  * injects the TACC-compiled OpenSeesPy library, and
  * launches your script (serial or MPI)
* Locating outputs and interpreting the **job summary log**

The emphasis is on **execution mechanics**, not OpenSees theory or model formulation.

---

## What This Notebook Does *Not* Cover

To keep the focus clear, this notebook intentionally does **not** cover:

* Writing or validating OpenSeesPy models
* Advanced MPI domain decomposition strategies
* Large-scale production workflows
* Custom SLURM scripting

Those topics are addressed elsewhere in the OpenSees-on-DesignSafe documentation.

---

## When to Use This Pattern

The workflow demonstrated here is well suited for:

* Training and tutorials
* Small-to-moderate OpenSeesPy analyses
* MPI-enabled OpenSeesPy scripts using 'mpi4py'
* Parameter studies and lightweight automation
* Users who want **no direct interaction with SLURM scripts**

If you later need more control over execution logic or scaling behavior, the same concepts shown here apply when moving to more specialized Tapis apps or custom workflows.

---

## How to Read This Notebook

You can follow this notebook in two ways:

* **Linearly**, as a step-by-step tutorial, or
* **Selectively**, using it as a reference when submitting your own jobs

Each section explains **why a setting exists**, not just what value to use, so you can confidently adapt the workflow to new problems.

