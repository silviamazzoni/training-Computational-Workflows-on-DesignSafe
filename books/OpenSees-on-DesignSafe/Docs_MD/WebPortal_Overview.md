# OpenSees from Web Portal  
*Hybrid Workflow with Web Portal + JupyterHub*

DesignSafe provides a suite of **Tapis-powered OpenSees applications** accessible through its **Web Portal**, allowing users to run both sequential and parallel jobs on Stampede3 **without writing SLURM scripts manually**. This section introduces the available apps, how they work, and how to integrate them into a **JupyterHub-driven workflow**.

## Available Applications

| App Name         | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **OpenSees-Express** | Sequential execution on a VM; great for small or test models.               |
| **OpenSeesMP**       | Parallel execution using MPI across multiple nodes for large simulations.  |
| **OpenSeesSP**       | Parallel static analysis (domain decomposition).                           |

These apps are backed by the **Tapis platform**, which handles job submission, staging, monitoring, and result retrieval from TACC systems.

## Why Use the Web Portal?

The Web Portal simplifies the entire HPC job submission process:

- Upload input files via a browser
- Select the app and main input script
- Configure compute settings (cores, wall time, etc.)
- Submit without writing a SLURM script

**Under the hood, the Web Portal:**

- Generates a SLURM job file
- Stages input files to Stampede3’s scratch space
- Launches the job using Tapis + SLURM
- Transfers output back to your **My Data** folder

| Without Web Portal App         | With Web Portal App                      |
|--------------------------------|------------------------------------------|
| Manual SLURM script writing    | Script auto-generated                    |
| Manual file transfers          | Input/output staged automatically        |
| Manual module setup            | Preconfigured compute environment        |
| Manual cleanup or downloads    | Output copied back to My Data            |

:::{note} 
For short jobs, Web Portal queue times and data transfers may dominate runtime. Use accordingly.
:::

## Recommended Workflow: Web Portal + JupyterHub

The most effective way to use DesignSafe's **web-portal apps** is to **combine them with JupyterHub** for a complete workflow:

* Use **JupyterHub** for interactive **pre-processing**: build and test your OpenSees models, edit input files, and visualize geometry.
* Then launch your simulation using a **DesignSafe web-portal app** (e.g., OpenSeesMP), which submits the job via SLURM to Stampede3.
* Once the job finishes, return to **JupyterHub for post-processing**: retrieve results, generate plots, compute summaries, or feed outputs into further analysis.

This hybrid workflow takes advantage of:

* The **user-friendly interface** and automated HPC submission of the web portal,
* And the **flexibility and power** of JupyterHub for coding, visualization, and iterative development.


## Summary

The **OpenSees Web Portal Apps** let you:

- Submit OpenSees jobs to Stampede3 without learning SLURM
- Easily switch between sequential and parallel workflows
- Combine the power of Jupyter for scripting and visualization with the Web Portal for scalable HPC execution
- Customize or automate workflows via Tapis (for advanced users)

Whether you're running one job or one thousand, this hybrid approach saves time, reduces errors, and allows you to focus on the science.
