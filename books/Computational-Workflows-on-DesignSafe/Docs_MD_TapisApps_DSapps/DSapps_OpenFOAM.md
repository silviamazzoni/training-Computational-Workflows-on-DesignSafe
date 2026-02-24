# OpenFOAM app

OpenFOAM is a powerful, open-source computational fluid dynamics (CFD) toolkit, widely used for modeling fluid flow, turbulence, heat transfer, and more. But running OpenFOAM on a large-scale HPC system like Stampede3 is **notoriously complex**, for several reasons:

* You typically work with **case directories** containing *system/*, *constant/*, and *0/* folders — these must be staged properly to the compute environment.
* Running in parallel requires careful setup with *decomposePar*, plus a correctly configured *SLURM* script that specifies the MPI processes and threads.
* After execution, you often need to reconstruct data (*reconstructPar*) and post-process, then gather results back into persistent storage.

Doing this manually means:

* Writing and testing your own SLURM batch scripts with the correct MPI parameters.
* Loading specific TACC modules for OpenFOAM (which may vary by cluster and compiler stack).
* Manually copying your case directory to the HPC’s scratch space to ensure the solver can read/write efficiently.
* Cleaning up large intermediate files and pulling final results back to long-term storage.

## The OpenFOAM app on DesignSafe simplifies this entire workflow

The **OpenFOAM Web-Portal app** on DesignSafe takes care of these complexities by:

* Accepting your **full OpenFOAM case directory**, packaged for upload.
* Automatically **generating the SLURM submission script** to run on TACC systems, with the correct *mpirun* or *srun* calls for your requested resources.
* Staging your case files to the HPC scratch space for maximum I/O performance.
* Executing your solver, then reconstructing the results (if required).
* **Copying the results back** to your DesignSafe workspace so you can download or continue post-processing.

This frees you to focus on **building and validating your CFD model**, not on the administrative overhead of HPC cluster workflows.

## Where to find the app’s code

Like all DesignSafe apps, the OpenFOAM application is fully open source. You can explore the implementation at [WMA-Tapis-Templates](https://github.com/TACC/WMA-Tapis-Templates/tree/main/applications).

There you’ll find:

* Input parameter schemas (describing what files and options you can set).
* Templates for SLURM submission scripts specific to OpenFOAM’s decomposition and parallel execution.
* Any container definitions or environment module setups used to ensure compatibility across TACC systems.

Studying this repository is an excellent way to understand **how your OpenFOAM inputs are translated into HPC jobs**, which is especially valuable when you start writing your own automation or direct SLURM submissions.

## Summary: why use the OpenFOAM app?

| Without the app                            | With the OpenFOAM app on DesignSafe             |
| ------------------------------------------ | ----------------------------------------------- |
| Manually prepare SLURM + MPI scripts       | SLURM + MPI setup done automatically            |
| Copy case files to scratch by hand         | Input cases staged for you                      |
| Must load modules and ensure correct build | Environment pre-configured on TACC              |
| Reconstruct + copy results back manually   | Outputs automatically gathered into **My Data** |
| Handle parallel decomposition explicitly   | Decomposition + execution managed by the app    |

The app ensures your CFD analyses run efficiently on HPC, without requiring you to become an expert in SLURM, MPI, or filesystem staging.
