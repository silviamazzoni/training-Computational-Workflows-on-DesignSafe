# HPC on TACC
***Understanding the TACC HPC Environment***

DesignSafe computations are powered by the **Texas Advanced Computing Center (TACC)**, which hosts world-class high-performance computing (HPC) systems like **Stampede3**, **Frontera**, and **Lonestar6**. These systems allow researchers to run simulations and workflows at a scale far beyond what's possible on a personal computer or basic virtual machine.

## What Makes HPC Different?

Unlike single-node environments like VMs or JupyterHub containers, HPC systems allow you to run simulations across **multiple compute nodes**, each with dozens of CPU cores and large amounts of memory. But it’s not just about node counts — HPC performance depends on:

* **Processor architecture and clock speed**
* **Cores per node** (e.g., 48–128)
* **Memory per node**, which may be fixed or configurable
* **Interconnect speed** between nodes (important for MPI-parallel jobs)
* **I/O performance** to and from large-scale parallel file systems

TACC systems are designed to optimize all of these aspects, supporting simulations and workflows that are compute- or memory-intensive, I/O-heavy, or parallelized across thousands of cores.


In HPC environments like TACC, jobs are submitted to a **scheduler** that manages resource usage across thousands of users. To make informed decisions about how to configure and run your jobs, it's important to understand the key components of this ecosystem.


## Interactive Sessions for Testing

Before submitting large production jobs, you can **connect interactively to the system** to test scripts, troubleshoot errors, or run small-scale jobs:

1. **SSH** into a TACC login node
2. Use `idev` to request an **interactive compute node**
3. Run commands in real time to debug, monitor, or explore

This is especially useful for:

* Validating SLURM scripts
* Troubleshooting runtime errors
* Checking CPU/memory usage

## File Movement and Data Staging

Your jobs **don’t run directly** from the DesignSafe **My Data** storage. Instead:

* Input files are staged to TACC’s **work** or **scratch** file systems -- data access is much faster this way.
* Output files are written to these systems and must be copied back afterward

DesignSafe simplifies this through:

* The **Web Portal**, which handles staging automatically
* **Tapis**, which automates job execution, file transfers, and cleanup

## CPU vs GPU Nodes

Some systems, such as **Frontera** or **Vista**, also offer **GPU nodes** that support deep learning and CUDA-enabled applications. These nodes are not typically used for OpenSees, but they are available for workflows involving image analysis, neural networks, or accelerated solvers.


---

We have introduced these concepts here because they will appear **again and again throughout this module**. This page serves as a **high-level reference** you can revisit anytime.

You’re welcome to jump into the sections below now to explore each concept in more detail—or simply return to them later as they come up in real examples.

