# Run Tapis Apps
***Run OpenSees Tapis Apps on DesignSafe as Examples***


Running OpenSees on a high-performance computing (HPC) system like Stampede3 isn’t as simple as just launching a command. DesignSafe has developed and published three official **OpenSees Tapis Apps** that automate all of this setup and submission:

* **OpenSeesEXPRESS** – for sequential simulations -- runs on a dedicated VM
* **OpenSeesMP** – for parallel simulations -- runs on Stampede3
* **OpenSeesSP** – for single-processor jobs -- runs on Stampede3


## The OpenSees app on DesignSafe automates OpenSees Jobs on TACC

The **OpenSees Web-Portal app** on DesignSafe does all of this heavy lifting. It:

* **Generates the SLURM job script for you**, tuned to the TACC environment (whether for *OpenSees*, *OpenSeesMP*, or *OpenSeesSP*).
* **Automatically stages your input files to the HPC scratch directory**, where I/O is fastest.
* **Executes your analysis** on the compute nodes you requested.
* **Collects and returns your output files to your DesignSafe My Data workspace** after the job completes.

This abstraction allows researchers to launch simulations efficiently—without writing job scripts or accessing the command line on a remote cluster. Whether you're working through the portal, a Jupyter notebook, or a custom workflow, the Tapis apps provide a consistent and scalable way to run OpenSees on TACC resources.

This means you can:

* Focus on your structural or geotechnical model — not on cluster commands.
* Submit jobs through a simple browser interface (or later, programmatically through Tapis or Python).
* Get consistent, optimized performance on TACC hardware without fighting with compilers, environment modules, or manual SLURM scripts.



## Why use the OpenSees app?

| Without the app                    | With the OpenSees app on DesignSafe              | What the Job Does |
| ---------------------------------- | ------------------------------------------------ | ----------------- |
| Write **SLURM batch scripts** by hand        | Automatically **Generates a SLURM script** tuned to TACC’s environment (for *OpenSees*, *OpenSeesMP*, or *OpenSeesSP*)                    | The script specifies resources, module loads, and MPI or OpenMP directives|
| Manually copy files to scratch     | **Stage your input files** from DesignSafe storage into *$SCRATCH* on Stampede3 for fastest I/O                            | Files are moved from your storage area to the cluster’s scratch space for speed|
| Worry about correct module loads   | Environment pre-configured. **Executes the analysis** with the requested cores, nodes, and wall time                       | Ensure your script requests the right cores/nodes so you neither waste allocation time nor hit resource limits|
| Track output files manually        | **Collects output files** from *$SCRATCH* and automatically returns them to your DesignSafe **My Data** workspace | Copy Files back from scratch to long-term storage |
| Manage tight coupling of resources | App sets up MPI/threads as needed                | Troubleshoot environment issues (e.g., making sure *OpenSeesMP* or *OpenSeesSP* is compiled and on your path)|

This process is essential for efficient HPC use but is also error-prone and requires familiarity with Linux, SLURM, and cluster architecture.

The app streamlines this entire process so you can **focus on your engineering analysis**, not on cluster logistics.

---
## Prerequisites

Before you begin:

* You have a **DesignSafe account**
* You are configured to use the **TACC Tapis tenant**
    You have established a TMS token -- this is done only once per system, and has been shown elsewhere in this training module.
* You’ve obtained an **access token** and instantiated a *Tapis* client -- you have connected to Tapis
* Your **input folder** is already uploaded to a Tapis-accessible system like *MyData*

## Example Input Directory Structure

As the very first step, Tapis moves your input directory into the execution directory, so you need a folder structure such as the following:

```
designsafe.storage.default:/myuser/projects/opensees-tests/run01/
├── model.tcl
├── loads/ground1.at2
└── params.txt
```

---

## Step-by-Step: How an OpenSeesMP Job Runs

1. **Job Definition**
    * Either fill out the **OpenSeesMP app form** on the DesignSafe WebPortal: select your input *.tcl* file, number of cores, wall time, etc.
    * Or in a **Jupyter Notebook** manually create a job-definition json object, with content similar to the web-portal input.
1. **Job Submission**
    * Once you click *Submit*, the DesignSafe WebPortal will **automatically** gather your input, create a job description and submits the job to Tapis.
    * Use the Tapis python API (tapipy) to submit your job-description object to Tapis manually. (This process will be shown in this training module)
3. **App Definition** – Tapis uses the app’s *app.json* and *profile.json* to configure the executable (*OpenSeesMP*), module loads, and file mounts.
4. **SLURM Script Built** – A *job.slurm* script is generated automatically using your inputs and the app template.
5. **Submission to TACC** – The job is submitted to **SLURM on Stampede3** via the Tapis Jobs API.
6. **File Staging** – Input files are copied from **My Data** to *$SCRATCH* for fast I/O.
7. **Job Execution** – SLURM launches the job using *ibrun OpenSeesMP mymodel.tcl*, running in parallel across N MPI processes.
8. **Output Collection** – Files (*.out*, *.err*, *.log*, or custom outputs) are gathered from *$SCRATCH*.
9. **Return to My Data** – Results are returned automatically to your **My Data** workspace for download or post-processing.

---

## Advantages for OpenSees Users

* No need to write or debug SLURM scripts.
* Module environments and MPI execution configured automatically.
* Runs on Stampede3’s production queues with efficient scaling.
* Files are staged and organized for performance and reproducibility.
* Outputs are returned directly to your workspace, ready for analysis.

:::{note}
Ideal for medium-to-large OpenSeesMP models and for researchers who want reproducible HPC workflows without deep SLURM knowledge.
:::

---
## Launching OpenSees Tapis Apps

You can launch the OpenSees apps in three ways:

:::{dropdown} DesignSafe Web Portal (Apps & Tools) — point-and-click

* Go to **Apps & Tools** → choose **OpenSeesEXPRESS**, **OpenSeesMP**, or **OpenSeesSP**.
* Fill in the app form: select your input file(s), set parameters (e.g., cores, wall time), pick the queue/system, and **Submit**.
* The portal builds a valid Tapis job request, stages inputs to the execution system (e.g., `$SCRATCH` on Stampede3), runs the job, and archives outputs back to **My Data**.
:::

:::{dropdown} Jupyter Notebook with Tapipy (Python SDK) — programmatic -- **Recommended and demonstrated here!!!**

* Best for automation, parameter sweeps, chaining pre/post-processing, and reproducible pipelines.
* Outline: authenticate → inspect the app to learn its parameters → build a job payload → submit → poll status → fetch outputs.

:::

:::{dropdown} Tapis CLI (or direct HTTP/cURL) — scripting & CI

* Use the CLI to submit JSON payloads from your terminal or CI pipelines.
* Typical flow mirrors the Python example: *tapis apps show*, prepare *job.json*, then *tapis jobs submit -f job.json*, followed by *tapis jobs output …* to retrieve results.
* This method gives you full control (and responsibility) for the entire job-submittal and file movement process.
:::

---

## Where to Find the DesignSafe app code

All OpenSees apps are **open source** and maintained in the [WMA-Tapis-Templates repository](https://github.com/TACC/WMA-Tapis-Templates/tree/main/applications).

There you’ll find:

* The core TACC app JSON definitions (describing inputs, outputs, and parameters).
* JSON input schema files (describing what inputs the app expects)
* Environment definitions (Docker/Singularity or module profiles).
* Examples of the underlying SLURM scripts it builds on your behalf, or submission logic.

This transparency lets you see exactly how your parameters translate into SLURM submissions, and how file staging is performed. Studying this repo is an excellent way to learn exactly how your inputs turn into HPC jobs, which helps when you want to move to more advanced workflows (like building your own SLURM scripts or automating with Tapis).


## Summary

This workflow allows you to:

* Programmatically submit OpenSeesMP jobs from Python
* Automate batch simulations or parametric sweeps
* Integrate with Jupyter Notebooks or external orchestration scripts
