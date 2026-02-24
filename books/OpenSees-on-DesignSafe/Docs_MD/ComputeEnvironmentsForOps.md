# Introduction

DesignSafe offers three compute environments for developing and running your Workflows:

* The **JupyterHub Environment**, an interactive containerized workspace
* The **OpenSees-Express VM**, a shared virtual machine accessed via the Web Portal or Tapis
* The **HPC Environment** at TACC, accessed SLURM scripts ( + Tapis), ssh, or Jupyter for HPC

Each serves a different purpose in the research workflow.

**NOTE** The Opensees Web Portal submits jobs to the HPC system, using **Tapis Apps** under the hood. So it falls under the "batch job" category, even though it's accessed through a graphical interface.


## Quick Tips

* JupyterHub is the most flexible environment — it supports OpenSees, OpenSeesMP, OpenSeesSP, and OpenSeesPy, with integrated file editing, scripting, and post-processing.
* OpenSees-Express is ideal for short Tcl jobs when you want **instant results** through a simple web form.
* HPC jobs (MP/SP) are best for large-scale work — and can be launched via the portal or automated from Jupyter.


