# Tapis Apps
**Tapis Applications are the foundation of the Tapis job workflow.** They enable consistent, portable, and sharable execution of complex analyses across compute systems.

**Tapis Apps** are pre-configured software templates that let researchers run simulations, analyses, and data workflows on high-performance computing (HPC) systems — **without needing to write job scripts or manage SLURM directly**. They encapsulate the executable, expected inputs/parameters, and the target execution system so you don’t have to write or maintain scheduler scripts.


A **Tapis App** is a preconfigured, reusable execution template that defines:

* The **executable** (binary program/script/container) to be run (e.g., OpenSees, OpenFOAM, custom scripts)
* What **inputs**, **parameters**, and **environment variables** it expects
* The **execution system** (like Stampede3) where the job should run
* The **runtime environment** which describes how the job should be launched (e.g., runtime settings, number of cores)

:::{card}
Apps decouple *what to run* from *where/how to run it*, so users don’t need to write scheduler scripts or manage modules. Most importantly, they allow researchers to focus on science, not infrastructure.
:::


---
## Why Use Tapis Apps?

* **Consistent UX:** same workflow across systems and schedulers.
* **Reproducible:** versions, defaults, and metadata are tracked.
* **Portable:** works from the Web Portal, Python (Tapipy), or CLI.

Tapis apps provide major benefits:

| Benefit                       | What It Does                                                                                 |
| ----------------------------- | -------------------------------------------------------------------------------------------- |
| **Simplifies HPC access**     | No need to SSH, stage files manually, or write job scripts                                   |
| **Standardizes environments** | Ensures the right modules, compilers, and binaries are used across all users                 |
| **Optimizes performance**     | Automatically runs jobs from fast storage (e.g., *$SCRATCH*) for best I/O performance        |
| **Automates file handling**   | Input/output files are transferred cleanly between your DesignSafe workspace and HPC systems |
| **Enables reproducibility**   | Job metadata and configuration are tracked and reproducible for later re-use                 |

This means researchers can focus on **engineering and science**, while Tapis ensures jobs are run efficiently and consistently across HPC systems.


---
## Which Apps to Use

You can use registered Tapis Apps (e.g., OpenSees, OpenFOAM), or you can write your own -- using a registered app as a tempate.

The registered apps are available through the **DesignSafe Web Portal**, or programmatically via **Jupyter notebooks** or the **Tapis CLI**. Each app encapsulates all the information needed to run a specific scientific application — such as **OpenSees**, **OpenFOAM**, or custom tools — using best practices for performance and reproducibility.

---

## What Do Tapis Apps Do?

When you submit a job via a Tapis App, the system automatically:

* **Generates a SLURM script** tailored to the app
* **Stages your input files** to the HPC system (e.g. *$SCRATCH*)
* **Submits the job** to the correct queue on a system like Stampede3
* **Runs the job** with the right environment, modules, and executable
* **Returns the output** back to your DesignSafe workspace (**My Data**)

*This process overlaps steps 4-6 in the Jub submittal described above. *

Tapis handles the technical complexity behind the scenes — including queueing, execution, module loading, and file movement — so you can focus on the science.

> Under the hood, your app submission becomes a SLURM batch job, executed on a system like **Stampede3** or **Frontera**.


---
## Typical Inputs to a DesignSafe Tapis App

Whether submitted through the web portal or programmatically, most apps expect:

* **Main input file** (e.g., *model.tcl* for OpenSees or *input.json* for a custom workflow)
* **Supporting files** (e.g., data sets, configuration files, libraries)
* **Run parameters** (e.g., number of cores, wall time, flags)
* **Output preferences** (optional controls over where and how results are returned)

Because the app handles the SLURM environment for you, **you don’t need to write a job script manually** — unless you want more advanced control.





