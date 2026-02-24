# OpenSees on JupyterHub
***The Primary Interface for Scripting, Testing, and Orchestrating Your Workflow***

The **DesignSafe JupyterHub** is your command center for running OpenSees in all its forms—whether you're writing Tcl scripts for the traditional interpreter or Python scripts using OpenSeesPy. It is the **primary portal for scripting, visualization, data management, and HPC job orchestration**.

This environment is ideal for:

* Interactive script development
* Pre- and post-processing of model data
* Exploratory analysis and documentation
* Submitting HPC jobs directly via the Tapis API

Each JupyterHub session runs in a dedicated container on a TACC-managed Kubernetes cluster, with **up to 8 CPU cores and 20 GB of RAM**—perfect for medium-scale simulations and full-featured development workflows.

All OpenSees have been pre-installed and are available in JupyterHub:
* Tcl: OpenSees, OpenSeesMP, and OpenSeesSP
* Pythong: OpenSeesPy

## Choosing the Right Interface for Your Task
    
JupyterHub offers a suite of interfaces tailored to different stages of your modeling and analysis process:

| Task                                   | Recommended Interface   |
| -------------------------------------- | ----------------------- |
| Running Tcl scripts                    | Terminal                |
| Running OpenSeesPy *.py* files         | Console or Terminal     |
| Exploratory modeling and visualization | Jupyter Notebook        |
| Editing scripts or organizing inputs   | File Editor & Manager   |
| Pre/Post-processing, automation        | Jupyter Notebook        |
| Submitting to HPC                      | Notebook with Tapis SDK |

Each of these interfaces is described below in more detail.

:::{dropdown} **Terminal-Based Workflow** -- Command-Line Interface (CLI)

* The **Terminal** interface replicates a traditional development environment and is well-suited for power users.
* You can execute OpenSees scripts using command-line syntax::

  * *OpenSees model.tcl* — run a Tcl script
  * *python model.py* — run an OpenSeesPy script
  * *mpirun -np 4 OpenSeesMP modelMP.tcl* — run a parallel OpenSees job
* Combine the terminal with the file editor and file manager to iteratively test, fix/modify, and rerun your scripts.
* Recommended for users who are familiar with command-line workflows or need to test parallel scripts.

:::

:::{dropdown} **Python Console**

* The **Python Console** provides interactive access to a Python interpreter.
* It’s a streamlined interface for:

    * Running *.py* files created outside of Jupyter (e.g., in VSCode or Spyder)
    * Interactive OpenSeesPy tests and quick calculations
    * Debugging one-liners and exploring external libraries
    * Running snippets without the structure of a notebook

* Example:
    ```python
    runfile('model.py')
    ```

This approach gives you real-time access to the Python interpreter without the overhead of a notebook.

:::

:::{dropdown} **Jupyter Notebook**
* Notebooks offer an **interactive, visual, and self-documenting** workflow.
* Best suited for OpenSeesPy users working with:

  * *matplotlib* or *plotly* for visualization
  * *pandas*, *numpy*, and *scipy* for numerical tasks
* Ideal for:

  * Educational content
  * Reports and documentation
  * Pre- and post-processing
  * Rapid prototyping and validation

* Caveats:
    While notebooks are powerful, they can introduce **execution overhead**, such as:
    
    * Kernel state inconsistencies (e.g., accidentally reusing stale variables)
    * Out-of-order execution confusion
    * Restart or dependency issues when migrating notebooks to batch workflows


:::


:::{dropdown} **Submit HPC Jobs Using Tapis**

When you’re ready to scale up your model, use the Tapis Python SDK (*tapipy*) or pre-built helper functions to:

* Submit jobs to Stampede3 or Frontera
* Monitor status and retrieve results
* Keep everything embedded within your notebook for seamless documentation and repeatability


:::

:::{dropdown} **File Editor & File Manager**

Use these built-in tools to:

* Edit scripts quickly
* Move, copy, and rename files
* Upload and download input/output data
* Set up your working directory for job runs

:::

:::{dropdown} **Pre- and Post-Processing with Python**

JupyterHub shines when paired with Python’s scientific libraries. Use this environment to:

* Generate parametric input files or signal data
* Analyze time histories, nodal displacements, stresses, etc.
* Build plots, reports, and interactive dashboards
* Automate workflows for sensitivity studies or optimization

:::

:::{dropdown} **Mix and Match Interfaces**

One of the biggest strengths of the Jupyter environment is its flexibility:

* Use the **file editor** to write and modify scripts
* Use the **terminal** for command-line execution and debugging
* Use a **notebook** for visualization, post-processing, and documentation
* Use the **console** for quick calculations or exploratory work

This layered interface model lets you tailor your workflow to your project phase — from early prototyping to full-scale automation.

:::

:::{dropdown} **Recommended Practice**: Modular Scripting with *.py* (and *.tcl*) Files

* Even if you use notebooks, it is best to maintain your OpenSees logic in standalone .py or .tcl files. Then:
   * Use %run, os.system(), or imports to call them in notebooks
   * Keep notebooks focused on post-processing, visualization, and documentation
   * Reuse scripts for both interactive and batch (HPC) runs without modification
* To avoid the pitfalls and support scalability, we recommend developing your OpenSees analysis in a standalone *.py* or *tcl* file, then integrating it into your notebook as needed.  This also allows you to integrate OpenSees-TCL into a jupyter notebook for pre and post-processing.

* Why this helps:

    * Cleaner organization
    * Promotes **modularity and version control**
    * Simplifies **debugging and testing**
    * Better portability for HPC and SLURM jobs: Makes it easier to **submit the same script to the HPC system**
    * Keeps your notebook focused on interpretation, documentation, and visualization

* Ways to call your *.py* or *.tcl* script from a notebook:
    
    | Method                   | Syntax                                                                 | How it works                                                                                                                                           |
    | ------------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | ***%run* magic command** | *%run my_model.py*                                                     | Executes the script **in the current notebook kernel**, preserving variables and imports — useful when you want to access or plot internal results     |
    | ***import* statement**   | *import my_model*                                                      | Imports the *.py* file like a library — runs once and allows access to functions or objects, but not standalone scripts with logic in the global scope |
    | ***os.system()***        | *os.system('python my_model.py')*<br>*os.system('OpenSees model.tcl')* | Executes the command **outside the notebook kernel**, like a terminal. Variables defined in the script are not accessible after execution              |
    
    You can also run **OpenSeesMP** (parallel jobs) using:
    
    ```python
    os.system('mpirun -np 4 OpenSeesMP modelMP.tcl')
    ```
    
    This approach makes it easier to:
    
    * Scale up by using the same *.py* in a **Tapis** job or **SLURM batch** script
    * Separate **computation logic** from **interface and visualization**
    * Minimize errors due to out-of-order execution
    
*  **Best Practice:**
    Develop in *.py* or *.tcl* scripts, test via terminal or *%run*, and document results in a clean, reproducible notebook.

:::

## Summary

The **DesignSafe JupyterHub** environment allows you to:

* Develop and test OpenSees models interactively
* Choose the interface that matches your workflow stage
* Submit HPC jobs programmatically
* Pre- and post-process data using modern Python tools
* Keep your full analysis pipeline in one environment

It is your **launchpad for scalable, reproducible OpenSees workflows**—whether you're just starting a model or scaling it to HPC.

Let me know if you'd like this formatted for Jupyter Book directly or split across multiple pages.
