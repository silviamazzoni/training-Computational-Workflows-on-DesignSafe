# DesignSafe Tapis Apps
***DesignSafe Simulation Apps: A Powerful Interface to HPC***

The DesignSafe platform offers web-based applications that bridge the gap between domain-specific scientific software and high-performance computing (HPC). Whether you're modeling earthquake effects on structures, simulating turbulent fluid flow, or forecasting coastal storm surge, DesignSafe’s simulation apps allow you to **leverage the computational power of TACC’s Stampede3 system**—without needing to write your own SLURM scripts or manage complex job submissions.

Currently, DesignSafe has three flagship apps:

* **OpenSees**: for structural and geotechnical engineering simulations,
* **OpenFOAM**: for computational fluid dynamics (CFD), and
* **ADCIRC**: for modeling coastal storm surge and hydrodynamics.

These apps are more than just wrappers around command-line tools—they’re **curated HPC workflows** that automate file staging, parallel execution, and result collection. Each is carefully constructed to match the typical needs of its user community, with differences in how they handle mesh decomposition, MPI job launch, or post-processing.

Whether you're a student learning simulation, a researcher submitting batch jobs, or an engineer running calibrated regional models, these apps make advanced computing **accessible, transparent, and reproducible**.



## Build On What You Will Learn

While this training module is focused on **OpenSees**, the principles extend to any scientific workflow you might run on DesignSafe. The app framework—using **Tapis for job submission**, **SLURM for HPC scheduling**, and the **Web Portal for user-friendly access**—is shared across all these tools. By understanding how these apps are structured and executed, you’re gaining insight into **general best practices for scientific computing on HPC systems**.

If your project requires a simulation tool not yet available as a DesignSafe app, you can build your own. Many researchers and teams have done exactly that—often by starting with one of these three as a template. We recommend choosing the app that most closely matches your problem type or parallel model (e.g., MPI-based for distributed jobs, thread-based for shared memory), then adapting it to your specific use case.

DesignSafe’s commitment to **open infrastructure** means you have access to the app source code, SLURM templates, environment setups, and submission logic via the [TACC GitHub organization](https://github.com/TACC/WMA-Tapis-Templates). These examples serve as **living documentation** and powerful starting points for custom workflows—whether you're doing ensemble runs, sensitivity studies, or scaling up to multi-node simulations.

By learning how to use and understand these apps, you're not just learning how to run OpenSees—you’re gaining **portable HPC skills** that apply to other simulation domains and tools, across many disciplines.


### Accessing the Apps
As is demonstrated in this document, these apps can also be accessed via the DesignSafe WebPortal or directly through tapis via CLI commands, or in a Jupyter Notebook.
