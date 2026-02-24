# JupyterHub Containers
***JupyterHub Containers = Kubernetes Cluster***

The DesignSafe **JupyterHub** operates on a Kubernetes-managed cluster at the Texas Advanced Computing Center (TACC), offering an interactive, scalable development environment that supports scripting, job orchestration, and visualization — all from your browser.

## What Is Kubernetes?

Kubernetes is a platform for managing containerized applications across clusters of servers. In this case, it ensures that each user’s Jupyter session runs in an **isolated container**, scheduled efficiently on shared compute nodes.

## Resource Allocation

* When you start a session, Kubernetes provisions a **dedicated container** with:

  * Up to **8 CPU cores**
  * Up to **20 GB of RAM**
* These resources are **exclusively allocated** to your session — no other users can access your container’s assigned CPUs or memory.
* The **underlying physical node** is shared across multiple containers, so **I/O operations** may experience minor contention under heavy load.

## Best Use Cases

* Development and testing of computational workflows
* Running your python scripts interactively
* Pre-processing input files and visualizing simulation output
* Automating job submissions to HPC using **Tapis**

## When to Transition to HPC

If your workload requires more memory, cores, or multi-node execution (e.g., OpenSeesMP), you should move to TACC’s HPC systems like **Stampede3**, submitting jobs via:

* Tapis from Jupyter
* Tapis Apps via the Web Portal
* Manual *sbatch* scripts over SSH

The JupyterHub environment offers an interactive and versatile platform that seamlessly bridges workflow development with Tapis-based HPC execution. Its tight integration and flexibility make it an ideal space for prototyping, testing, and scaling analyses — from initial development to full production workflows.
