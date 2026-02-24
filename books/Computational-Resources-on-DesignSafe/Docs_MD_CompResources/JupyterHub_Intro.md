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

## Performance and Resources

* Jupyter Hub supports **Python**, **Julia**, **MATLAB**, and **R** — useful for researchers integrating multi-language workflows.
* Each Jupyter session runs in its own **container**, orchestrated by Kubernetes. The system guarantees:

* Up to **8 CPU cores** and **20 GB of RAM** per user session
* **Exclusive use** of these resources within your container (not shared with other users)
* Shared physical nodes underneath, which may cause **minor I/O contention** under heavy load

This environment is optimized for:

* Interactive model development
* Small to medium-sized simulations
* Pre- and post-processing of data
* Batch job submission to HPC systems

## Summary

The **DesignSafe Jupyter Hub** is a powerful entry point into workflows. It offers dedicated computing resources in an easy-to-use environment where you can:

* Develop, debug, and run your scripts in real time
* Automate job submission to HPC systems like Stampede3
* Perform pre- and post-processing without leaving the notebook interface

Use it as your **launchpad for scalable computation**: once your workflow is ready, move to HPC for large-scale runs without leaving Jupyter.
