# OpenSeesMP App

***Parallel OpenSees Runner for High-Performance Computing***

The **OpenSeesMP** app is a Tapis-powered, SLURM-submitted application that runs OpenSees in **MPI-parallel** mode on the **Stampede3 cluster** at TACC. Unlike *OpenSees-express*, this app is built for large-scale, multi-core structural simulations that require distributed memory processing, job queuing, and access to advanced hardware.

You can find the template for this app in the [TACC Repo](https://github.com/TACC/WMA-Tapis-Templates/tree/main/applications/opensees-mp/opensees-mp-s3)

## Key Features

* **Runs OpenSeesMP** — the MPI-enabled version of OpenSees
* **Executes on Stampede3** via SLURM scheduler
* **Leverages Tapis API** for structured job submission and tracking
* **Accepts directory-based input** with customizable *.tcl* scripts
* **Supports MPI execution** using *ibrun* across 2+ nodes and 48+ cores per node

This app is composed of three main files:

1. A Tapis *app.json* file defining the HPC job structure
2. A *profile.json* that loads Stampede3 modules
3. A *tapisjob_app.sh* script that launches the MPI-enabled binary




## Summary: OpenSees at Scale with OpenSeesMP

| Component         | Purpose                                                               |
|------------------|-----------------------------------------------------------------------|
| *app.json*        | Describes inputs, parameters, HPC config, and output archiving        |
| *profile.json*    | Loads required software modules on Stampede3                          |
| *tapisjob_app.sh* | Executes OpenSeesMP using *ibrun* and user-defined *.tcl* script      |

This app is ideal for:

- **Large-scale simulations** requiring distributed memory
- **Parallel analyses** using OpenSeesMP
- Users familiar with MPI and SLURM workflows

```{tip}
To **debug or test** your script before submitting to Stampede3, you can use the lightweight *OpenSees-express* or a JupyterHub terminal session with a smaller *.tcl* input file.
```
