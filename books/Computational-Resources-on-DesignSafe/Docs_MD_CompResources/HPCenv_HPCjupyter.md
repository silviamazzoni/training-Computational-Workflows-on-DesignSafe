# DesignSafe's HPC Jupyter Lab
**Interactive Jupyter on Stampede3 Compute Nodes**

DesignSafe now offers a powerful interface for working directly on HPC resources:
**JupyterLab HPC (CPU)**, **JupyterLab HPC (GPU)**, and **Jupyter HPC Native**. These options may grow and/or evolve over time.

Although these environments were originally introduced to support machine learning workflows, they are also ideal for users running OpenSees, Python-based simulations, or other research code that benefits from **interactive access to full compute nodes**.


## What Makes This Different?

When you launch a **JupyterLab HPC (CPU)** session, you are **not on a login node or a virtual container**. Instead:

> **You're running a full interactive Jupyter environment on a dedicated Stampede3 compute node.**

You may see the message:

> *“You are running an interactive Jupyter instance on a Stampede3 compute node.”*

This means:

* SLURM has queued and scheduled your session like any HPC job.
* You’ve been assigned a **full physical node** with exclusive access.
* You get all the **CPU cores** and **memory** of that node — no sharing with other users.



## Key Features and Behavior

| Feature                   | Description                                                                                |
| ------------------------- | ------------------------------------------------------------------------------------------ |
| **Real HPC node**         | You’re running directly on a Stampede3 compute node, not a container or shared login node. |
| **SLURM-scheduled**       | Your session waits in the SLURM queue, just like a batch job.                              |
| **Full-node access**      | You get exclusive use of all CPU cores and memory on the assigned node.                    |
| **Home directory access** | You can use your `$HOME` to store and reuse software environments (no need to reinstall).  |
| **Session limits**        | Maximum runtime is **48 hours**. For faster access, use the `skx-dev` queue (2-hour max).  |
| **All node types**        | You can launch sessions on any node type available on Stampede3.                           |



## Why Use JupyterLab HPC?

This environment is ideal when you:

* Want to **test and debug** scripts interactively before submitting full-scale SLURM jobs.
* Need to **analyze large output files** immediately after a run.
* Are running workflows like **OpenSeesPy**, data visualization, or parameter studies that benefit from live feedback.
* Prefer the **Jupyter interface** but want the **performance and consistency** of real Stampede3 hardware.

It gives you the best of both worlds:
💻 **Interactive development** with 🖥️ **high-performance compute resources**.



:::{admonition} Quick Tip: Faster Access for Testing

To reduce wait time while testing:

```bash
# Use the skx-dev queue (2-hour interactive session)
```

Choose `skx-dev` when launching your session to gain access faster (especially during peak usage periods).

:::


## Choosing Between JupyterHub and JupyterLab HPC

| Feature                 | **JupyterHub (Standard)**                               | **JupyterLab HPC (CPU/GPU)**                                     |
| ----------------------- | ------------------------------------------------------- | ---------------------------------------------------------------- |
| **Environment**         | Shared container environment                            | Dedicated compute node on Stampede3                              |
| **Startup Time**        | Immediate (on demand)                                   | Delayed (submitted through SLURM queue)                          |
| **Resources**           | Shared container: 8 cores, 20 GB RAM                    | Full node: up to 56 cores, 192 GB RAM (varies by node type)      |
| **SLURM Involvement**   | None (runs on Kubernetes-managed cluster)               | Yes — session is a queued SLURM job                              |
| **Maximum Runtime**     | No hard limit                                           | 48 hours (enforced by SLURM)                                     |
| **Best For**            | Lightweight scripting, plotting, Jupyter notebooks      | Large computations, OpenSeesPy, post-processing, ML workloads    |
| **Storage Access**      | `$HOME`, `$WORK`, `$DESIGNSAFE`, and persistent volume  | Full access to `$HOME`, `$WORK`, `$SCRATCH` on Stampede3         |
| **Custom Environments** | Requires reinstallation each session (unless in \$HOME) | Environments persist in your `$HOME` — no need to reinstall      |
| **Wait Time**           | None                                                    | Possible queue time depending on system load                     |
| **Use Cases**           | Prototyping, scripting, small jobs                      | Full-node testing, heavy computation, live debugging of HPC jobs |

---

## Summary

Use **JupyterHub** when:

* You need fast, interactive sessions
* You're working on smaller scripts or visualizations
* You don't need full-node performance
* You're working on larger jobs and are using JupyterHub as a **portal** to submit a SLURM job to HPC via tapis.

Use **JupyterLab HPC** when:

* You want to test or debug in a true HPC environment
* You need full access to Stampede3 resources
* You're running heavier workflows (e.g., OpenSees, ML training, large post-processing)

:::{tip}  
**Weigh the 48-hour time limit and possible queue wait against your project’s needs** to choose the right tool for each phase of your workflow.
:::


## Learn More

For detailed instructions on how to launch and manage HPC Jupyter sessions, visit the
[DesignSafe HPC Jupyter Guide](https://www.designsafe-ci.org/user-guide/tools/jupyterhub/#designsafe-hpc-jupyter-guide)

