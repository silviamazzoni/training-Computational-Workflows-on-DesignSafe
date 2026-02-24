# Anatomy of a Tapis App

A Tapis v3 App is built from a small set of core components that together define:

* how the app is described and registered
* how the environment is prepared on the compute node
* how your scientific workflow is executed
* how input and output files are staged

This chapter breaks down each component and explains its purpose and place in the runtime sequence.

---

:::{dropdown} **1. *app.json* — App Definition**

This is the **primary Tapis application definition file**. It contains all the top-level metadata and job configuration used by the Tapis Jobs API, including:

* The app ID, version ("latest"), and description
* Runtime type and container image (*ZIP*, containerImage)
* Execution system and directory paths (e.g., *${JobWorkingDir}*)
* Job submission type and resource requirements (e.g., node count, cores per node, memory, wall time) 
* Inputs and arguments required to run the application (input parameters and file requirements)
* Archive and output settings
* Tagging and user interface notes and options

This file is used by Tapis to register the app and to describe how it should be executed on the target HPC system.
Essentially, *app.json* tells Tapis **what this app is, how to run it, and what inputs/outputs to expect**.


:::

:::{dropdown} **2. Scheduler Profile — System-Level Environment Initialization**

A scheduler profile configures the compute node *before* your app runs.

It determines:

* The base environment (clean or preloaded)
* Whether the *module* command exists
* Default compiler/Python/MPI environment
* How SLURM launches the job

The apps in this notebook use:

```
--tapis-profile tacc-no-modules
```

This ensures a clean environment so the wrapper script controls all modules.

**Sidebar — Scheduler Profiles vs envVariables:**

* **Scheduler Profile** → configures *the system*
* **envVariables** → configures *your app’s behavior*

:::

:::{dropdown} **3. ZIP Runtime Package**

Each app is delivered as a single ZIP file stored in DesignSafe storage:

```
designsafe.storage.default/.../appname/version/app.zip
```

At job runtime, Tapis:

1. Copies the ZIP into the job working directory
2. Unpacks it
3. Executes the wrapper script inside

This ZIP functions like a simple container image.

:::

:::{dropdown} **3a. tapisjob_app.sh — Wrapper Script**
The wrapper script is contained in the ZIP Runtime Package.

This script contains all runtime logic:

* Logging and timers
* Normalizing python/python3
* Loading modules (OpenSees, python, HDF5…)
* Installing Python packages
* Copying OpenSeesPy (*OpenSeesPy.so*) if requested
* Optionally unzipping inputs
* Choosing launch method (*ibrun* vs direct execution)
* Running the user’s script
* Cleaning up
* Producing summary logs

This is the true **entry point** for the app.

:::

:::{dropdown} **4. *ReadMe.md* — App Documentation (Optional)**

Although optional, including documentation improves:

* transparency
* reproducibility
* ease of use in the DesignSafe portal

This file does not affect execution, but it is included in the ZIP bundle.

:::

:::{dropdown} **5. Input Directory (user provided)**

Each app declares one required input directory.

This directory must contain:

* The user’s main script (Tcl or Python)
* Supporting files
* Data files
* Requirements or module files (if used)

Tapis stages this directory to the job working directory before execution, and the wrapper script uses it as the run directory.

:::

---

## Runtime Sequence Overview

```
app.json → job submission → Tapis validates job → input staging → unpack ZIP
→ execute wrapper script → executes main program (launch user code) → archive outputs


                      ┌────────────────────────┐
                      │      Tapis App         │
                      │      (Registered)      │
                      └──────────┬─────────────┘
                                 │
          ┌──────────────────────┼────────────────────────┐
          │                      │                        │
   ┌──────▼───────┐      ┌───────▼────────┐      ┌────────▼─────────┐
   │   app.json   │      │ Scheduler      │      │  ZIP Package     │
   │ (definition) │      │   Profile      │      │  (runtime image) │
   └──────┬───────┘      │ (system init)  │      └──────┬───────────┘
          │              ┌┴───────────────┐          ┌──┴─────────────┐
          │              │ tacc-no-modules│          │ tapisjob_app.sh│
          │              └───┬────────────┘          │ + README.md    │
          │                  │                       └────┬───────────┘
          │                  │                            │
          ▼                  ▼                            ▼
  Defines inputs,     Loads system-level        Actual runtime logic:
  parameters, queue,  environment rules.        modules, pip, OpenSeesPy,
  environment, ZIP.                             launches the user script.

          ┌─────────────────────────────────────────────────────────────┐
          │                     Input Directory                          │
          │ (user-provided scripts, models, data, ZIPs, req files)      │
          └─────────────────────────────────────────────────────────────┘

                              Runtime Flow
                              ─────────────
              app.json → Tapis → unpack ZIP → run wrapper → run script
```

