# JupyterHub Environment
***Build and Test Your OpenSees Scripts with Flexibility and Speed***

The **JupyterHub Environment** on DesignSafe runs on a Kubernetes-managed cluster at the Texas Advanced Computing Center (TACC). It provides a highly accessible, interactive platform for developing, testing, and refining OpenSees scripts—whether you're using Tcl, Python (OpenSeesPy), or both.

This environment is the **starting point *(and end point)* for most workflows**. It allows you to iteratively build and test your input scripts in real time before scaling up to HPC batch jobs.

## Why Use Jupyter Hub?

* **Immediate startup** — no job queues or allocation requests
* **Full control and feedback** — ideal for debugging, exploration, and visualization
* **Integrated tools** — notebook interface, terminal, file manager, code editor, and Python console
* **Supports OpenSees, OpenSeesMP/SP, and OpenSeesPy**, plus other languages (MATLAB, Julia, R)
* **Direct connection to Tapis** — submit HPC jobs from within the notebook

## Ways to Run OpenSees Inside Jupyter Hub

You can run OpenSees in a variety of flexible ways from within this environment:

1. **Run OpenSees at the Terminal**

   Launch any Tcl or Python OpenSees script interactively using the terminal.
   
   → This is your **recommended starting point** if it is a natural transition from your personal desktop.

3. **Run OpenSeesPy in a Jupyter Notebook**

   Embed scripts and results in a single document for reproducibility and sharing.

5. **Run Tcl or Python OpenSees via `os.system()`**

   Execute command-line jobs from within a Python notebook. Works for both sequential and parallel jobs.

   * Note: `%run` can also work, but doesn’t accept variable substitution.

7. **Run OpenSeesPy in the Python Console**

   Useful for quick one-liners, loading external modules, or running python scripts you had developed on your desktop in Spyder or another IDE.

9. **Pre- and Post-Process Your Models**

   Use Python, NumPy, Pandas, Plotly, and other libraries to prepare inputs or analyze results.

11. **Submit HPC Jobs Using Tapis**

    Automate job submission from notebooks using the Tapis Python SDK (Tapipy) or helper functions.

13. **Use the Integrated File Editor and Manager**

    Quickly edit your input files or scripts and organize your workspace.

14. **Upload and Download Files with the Uploader Tool**

    Manage your working directory and sync files from external sources.

## Summary

The **DesignSafe Jupyter Hub** is a powerful entry point into OpenSees workflows. It offers dedicated computing resources in an easy-to-use environment where you can:

* Develop, debug, and run OpenSees scripts in real time
* Automate job submission to HPC systems like Stampede3
* Perform pre- and post-processing without leaving the notebook interface

Use it as your **launchpad for scalable computation**: once your model is ready, move to HPC for large-scale runs without leaving Jupyter.
