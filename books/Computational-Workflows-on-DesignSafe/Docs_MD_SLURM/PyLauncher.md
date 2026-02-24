# PyLauncher
***Running Parameter Studies with PyLauncher (Basic Usage)***

PyLauncher is a lightweight task launcher developed at TACC for running **many independent jobs within a single SLURM allocation**. It is especially useful for *parameter studies*, *sensitivity analyses*, and *embarrassingly parallel workloads* where each run is independent .

Instead of submitting dozens (or hundreds) of separate SLURM jobs, PyLauncher allows you to submit **one SLURM job** and execute a list of commands concurrently across the allocated cores. On DesignSafe, PyLauncher integrates cleanly with OpenSeesPy and can be used from the Portal, JupyterHub, or a notebook-driven workflow.

This section documents **basic PyLauncher usage only**, using the `ClassicLauncher`. MPI-enabled launchers are out of scope here and require additional configuration and testing.




---

## When to Use PyLauncher

Use PyLauncher when:

* You have **many independent OpenSeesPy runs**
* Each run is **serial (no MPI)**
* Each run can write its output to a **separate directory**
* You want to efficiently use allocated cores inside a single SLURM job

Do **not** use PyLauncher if:


* Your runs depend on shared output files
* You need tight inter-process communication

If you model requires MPI, use more advanced pylauncher options, which are beyond the scope of this document.

---

## Basic PyLauncher Workflow


### 1. Create the PyLauncher Input Script

Your main Python script should contain only the PyLauncher invocation:

```python
import pylauncher

pylauncher.ClassicLauncher(
    "runsList.txt",
    debug="host+job"
)
```

Notes:

* The `debug` option is optional and can be removed once things are working.
* This script **does not** run OpenSees directly — it only launches the commands listed in `runsList.txt`.

---

### 2. Create the `runsList.txt` File

The `runsList.txt` file contains **one command per line**, exactly as you would run it from the command line.

Example:

```text
python Ex1a.Canti2D.Push.argv.tacc.py --NodalMass 11.79 --outDir outCase39
python Ex1a.Canti2D.Push.argv.tacc.py --NodalMass 11.99 --outDir outCase40
python Ex1a.Canti2D.Push.argv.tacc.py --LcolList 100,200,300 --outDir outCase41
python Ex1a.Canti2D.Push.argv.tacc.py --LcolList 105,205,305 --outDir outCase42
python Ex1a.Canti2D.Push.argv.tacc.py --LcolList 110,210,310 --outDir outCase43
```

Important requirements:

* **Each command must write to its own output directory**
* Output directories should be specified explicitly (e.g., `--outDir outCaseXX`)
* Command-line arguments can be passed normally, including lists

---

### 3. Submit the Job

You may submit the SLURM Job in one of two ways:
* Manually -- you write your own SLURM-job file and submit it via sbatch from a login node
* Via Tapis App. The tapis apps build the SLURM-Job file and submit the job for you.

#### 3a. When Using a Tapis App
* If using OpenSeesPy, use the **OpenSeesPy app** on DesignSafe, otherwise use the **DesignSafe Agnostic app**, which offers offers many additional features.
* *UseMPI = false* when submitting the job to the Classic Launcher.
You may submit the job:

* Through the **DesignSafe Portal**
* From **JupyterHub**
* From a **Jupyter notebook**

Key settings:

* `UseMPI = false`
* Request enough cores to accommodate the number of concurrent tasks you want PyLauncher to run

---

## Output and Runtime Behavior

A few important things to be aware of:

* Each PyLauncher task runs in its **own temporary working directory**
* Results are copied back to the specified output directories when complete
* PyLauncher creates a **subdirectory inside your `inputDirectory`** that contains:

  * Per-task stdout
  * Per-task stderr
  * Launcher bookkeeping files
 
--> Launcher creates MANY files.

### Logging Behavior

* Your script's output **does not appear directly** in *tapisjob.out*
* Instead, logs are written to **individual files** inside the PyLauncher directory
* These files typically **do not have extensions**

⚠️ **Recommendation:**
Inspect PyLauncher output files using **JupyterHub**, as the Data Depot preview may not interpret these files correctly.

---

## How PyLauncher Fits into a SLURM Job


At a high level, PyLauncher runs *inside* a single SLURM allocation. SLURM provides the compute resources, and PyLauncher manages how individual serial tasks are dispatched across those resources.

Conceptually, the flow is:

1. **SLURM job starts**
   Resources (nodes and cores) are allocated by SLURM.

2. **PyLauncher is invoked**
   The `ClassicLauncher` reads a list of commands from `runsList.txt`.

3. **Independent tasks are executed**
   Each command is launched as a separate serial process, using available cores.

4. **Temporary execution directories are used**
   Each task runs in its own isolated working directory.

5. **Results are copied back**
   Output files are written to user-specified directories (e.g., *outCaseXX*).

This model avoids repeated queue waits and allows efficient use of allocated resources for large parameter studies.


---
## Practical Notes and Limitations

* Each task must be **file-system isolated**
* Shared writes will cause race conditions or data loss
* PyLauncher is ideal for *parameter sweeps*, not tightly coupled workflows
* MPI-enabled PyLauncher workflows require additional investigation and are not covered here

---

## Key Takeaway

> **PyLauncher is the supported task launcher at TACC for running multiple serial jobs within a single SLURM allocation.**

* The legacy launcher is deprecated and being retired
* PyLauncher is actively supported and maintained
* MPI modes exist but are not documented here
* For serial parameter studies, `ClassicLauncher` is the recommended and stable approach


---

## Summary

PyLauncher provides a simple and effective way to run many independent OpenSeesPy simulations within a single SLURM job. By combining a command list (*runsList.txt*) with the *ClassicLauncher*, you can efficiently scale parameter studies without the overhead of MPI or multiple job submissions.

If you stay within the serial-use model and ensure clean output separation, PyLauncher is a powerful and reliable tool for large batch studies on DesignSafe.

---

:::{dropdown} Launcher Support Status at TACC

**Important:**
The **legacy (old) TACC launcher** is **no longer supported** and is being **phased out across all TACC systems**. Users should **not rely on the old launcher** for new or existing workflows.

**PyLauncher is the supported replacement** for launching multiple tasks within a single SLURM allocation on TACC systems, including those accessed through DesignSafe.

If you encounter older documentation or examples referencing the legacy launcher, those materials should be considered **deprecated**.

:::


:::{dropdown} MPI Usage and Scope of This Documentation

PyLauncher **does support MPI-enabled execution modes**, and these can be used to launch MPI tasks under certain configurations.

However:

* MPI-enabled PyLauncher workflows require **additional setup**
* They involve tighter coordination with SLURM and MPI runtimes
* They require **careful validation and testing**

➡️ **MPI usage with PyLauncher is intentionally not covered in this documentation.**

This section focuses exclusively on:

* The **ClassicLauncher**
* **Serial, independent tasks**
* Reliable and reproducible parameter studies

If your workflow requires MPI:

* Use a native MPI job configuration, **or**
* Treat PyLauncher’s MPI modes as **advanced usage** outside the scope of this guide
:::
