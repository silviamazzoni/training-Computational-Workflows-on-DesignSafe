# Inputs for OpenSees Apps

Before diving into the details of the OpenSees Apps, it’s important to understand how **Tapis Apps** define their inputs in general.

Each Tapis app is published with a **schema** — a hierarchical JSON object that describes what inputs are available, which ones are required, and what defaults or constraints apply. To determine the inputs for an app, the workflow is:

1. **List available Tapis apps** – Use Tapis commands to display the apps currently available, along with their latest versions. Always select the **latest version** of an app for your runs.
2. **Retrieve the app schema** – Once you know which app and version you are using, fetch the schema. This tells you exactly which inputs you must (or can) provide.

I’ve created **two Jupyter Notebooks** to demonstrate these steps:

* One lists the available apps and their versions.
* Another retrieves and displays the schema for a selected app.

---

## Types of Inputs

When examining an app schema, you will encounter different kinds of inputs:

* **Hidden inputs** – Fixed values you cannot change and do not need to supply.
* **Fixed inputs** – Values you must include in the job-submittal file, but which cannot be altered.
* **Required inputs** – Inputs that must be provided by the user (e.g., the input directory and main input script).
* **Optional inputs** – Inputs with default values that you may override if needed (e.g., the archive directory).

---

## Structure of the Schema

At the top level, an app schema includes general, app-specific keys that define the app but are usually not editable. The most important section is the ***jobAttributes*** object, which contains several subsections:

* **Execution parameters** – Keys like *archiveSystemDir*, *nodeCount*, and *coresPerNode* can be set or overridden. Special care is needed with flags such as *isMpi*: this controls whether the *inner bash script* is run with MPI, not whether OpenSees itself is parallel.
* ***fileInputs*** – A list of inputs related to file staging. This is where you define the input directory to be copied into the execution environment.
* ***parameterSet*** – Application-specific inputs. For *OpenSeesMP* and *OpenSeesSP*, this includes the **program name** (fixed and hidden) and the **main script name** (REQUIRED).
* ***envVariables*** – A list of environment variables passed to the execution environment. For example, the *OpenSeesEXPRESS* app uses this object to define its input arguments.

⚠️ **Note on keys:** Different apps — and even different input objects within the same schema — may use different key-value pair formats. For example, some use *"key"* and *"value"*, while others use *"name"* and *"arg"*. This inconsistency can lead to errors if you are hand-writing JSON input.

---

## Tapis Paths

When specifying files and directories, Tapis expects **Tapis-style paths**, which point to locations in your DesignSafe storage systems (e.g., *MyData*, *MyProjects*, or *CommunityData*). These paths must be correctly formed for Tapis to locate and transfer your input files.

Because the full input directory is copied to the execution system and later returned to an archive directory, accurate path specification is critical.

---

## How Apps Run

Each Tapis app has **two main parts**:

1. **The SLURM job setup** – Defines job configuration (nodes, wall time, modules to load, etc.).
2. **An app-specific script** – Sets up additional parameters and calls OpenSees at the end.

You can inspect these scripts on GitHub if you are curious, but you generally do not need to. They are designed to consume the inputs defined in the schema, so providing the correct schema-based inputs is enough.

---

## OpenSees App Inputs

Because the OpenSees Apps run on different systems and were developed by different teams, the required inputs — and where they appear in the job-submittal file — vary slightly between apps. The *OpenSeesMP* and *OpenSeesSP* apps share the same input structure, while *OpenSeesEXPRESS* uses a different format.

In general, there are **two categories of inputs** you will need to provide:

1. **Job configuration inputs** – These specify how the job is executed on the HPC system (e.g., number of nodes, processors per node, and wall time). These inputs apply only to the *Stampede3 apps* (*OpenSeesMP* and *OpenSeesSP*) since they run through the SLURM scheduler.

2. **Run-specific inputs** – These tell the app which folder to copy into the execution directory and which OpenSees script to call.

---

## The Input Directory

The **input directory** is one of the most important inputs to define. The *entire directory* you specify is copied to scratch on the execution system before the run begins, and copied back after the run completes.

⚠️ **Important:** Most of the total runtime for small-to-medium jobs is often spent in **file transfer**, not computation. Since Tapis copies files one at a time, you should keep the number of files in your input directory to a minimum to avoid long transfer delays.

After execution, the folder is not restored to its original location. Instead, it is returned to an **archive folder** — either a location you specify, or the default directory in:

```
MyData/tapis-jobs-archive
```

---

## Submitting Inputs

All of these inputs are passed through the standard **Tapis job-submittal commands**. However, because of schema complexity, inconsistent key-value formats, and the use of Tapis paths, writing job submission files directly in JSON can be tedious and error-prone.

To address this, we provide a **Python wrapper function**. It allows you to define a simple Python dictionary of inputs, and then automatically converts it into the correct JSON format for Tapis. This both streamlines the workflow and reduces the chance of mistakes.

---

### Note

Although the details above are focused on OpenSees, the same principles apply to most **Tapis Apps that submit jobs through SLURM**. The schema structure, types of inputs, path conventions, and file handling are broadly consistent across applications.

