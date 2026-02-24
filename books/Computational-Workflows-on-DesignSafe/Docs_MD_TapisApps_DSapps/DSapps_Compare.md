# Compare Apps
***Comparing the OpenSees, OpenFOAM, and ADCIRC apps on DesignSafe***

The following comparison highlights both the shared foundation and distinct execution logic of the three DesignSafe applications -- OpenSees, OpenFOAM, and ADCIRC. Understanding these differences can help you choose the right tool, tailor your workflow, or even extend the apps to meet your advanced needs.


## What they have in common

All three apps are designed to make **high-performance computing (HPC) accessible from a simple web interface**, so you can focus on your engineering or science problem, not the logistics of running jobs on Stampede3 (or similar systems). They all:

* Let you upload your inputs through the **DesignSafe Web Portal**,
* Automatically generate the appropriate **SLURM job scripts**,
* **Stage your files to scratch** on the HPC system for maximum I/O performance,
* Execute your analysis, and
* Bring the results back to your **My Data** workspace on DesignSafe.

They also all:

* Use **Tapis under the hood** for secure job submission and data transfers,
* Rely on TACC’s fair-share scheduler,
* And are open source, hosted in the **DesignSafe GitHub organization**.

## How they’re implemented differently

| App          | How it’s structured under the hood                                                                                                                                                                   | What it automates specifically                                                                                                         |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **OpenSees** | Very lightweight JSON definitions that link to specific TACC-installed executables (*OpenSees*, *OpenSeesMP*, *OpenSeesSP*). Relies heavily on simple SLURM templates.                               | Generates a standard SLURM script and runs the correct binary. Copies input files to scratch, executes, and retrieves results.         |
| **OpenFOAM** | Includes extra steps to handle decomposition (*decomposePar*) before the main solver and reconstruction (*reconstructPar*) afterward. The app JSON and SLURM templates explicitly incorporate these. | Automates multi-step CFD workflow: decomposes mesh, runs parallel solver, then reconstructs results — all in scratch.                  |
| **ADCIRC**   | Tailored SLURM scripts that emphasize large-scale MPI runs across many nodes. Often includes environment modules and scratch staging optimized for massive runs.                                     | Sets up MPI execution across hundreds/thousands of cores, stages forcing and mesh files, and gathers huge result sets back to My Data. |

## Why this matters for advanced users

Knowing these differences helps you:

* **Debug or extend workflows** — e.g. if you want to move to direct SLURM submissions, you can look at the app’s GitHub repo to see exactly what it’s submitting.
* **Customize for ensembles or parameter studies** by borrowing the app’s staging logic or SLURM structure.
* **Understand performance trade-offs**, like why OpenFOAM must do decomposition/reconstruction, or why ADCIRC scripts are designed for extremely large MPI runs.

## Quick summary table

| App          | Target problems                    | Parallel model used                      | Special stages                                | Typical scale                         |
| ------------ | ---------------------------------- | ---------------------------------------- | --------------------------------------------- | ------------------------------------- |
| **OpenSees** | Structural & geotechnical analysis | MPI (OpenSeesMP) or threads (OpenSeesSP) | None beyond scratch staging                   | From single core to hundreds          |
| **OpenFOAM** | CFD (fluid flow, turbulence)       | MPI                                      | *decomposePar* before, *reconstructPar* after | Typically dozens to hundreds of cores |
| **ADCIRC**   | Coastal surge & hydrodynamics      | Large-scale MPI                          | Handles huge meshes & forcing files           | Hundreds to thousands of cores        |



### Next level: use the apps as your HPC recipe

Even if you ultimately move to more manual workflows (writing your own SLURM scripts for maximum control or using *t.jobs.submitJob* via Tapis), the DesignSafe app repos are an **excellent starting point**. They show:

* The exact modules and environment settings required on TACC clusters.
* Typical *srun* or *mpirun* patterns for large parallel jobs.
* File staging best practices (why everything goes to scratch first, then returns).

This means you can use these apps **as living examples of best practices for each software stack**, adapting their logic to scale up your work beyond what the simple Web Portal allows.


