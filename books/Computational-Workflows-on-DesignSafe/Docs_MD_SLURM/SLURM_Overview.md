# Job Overview
***How Are Jobs Run for DesignSafe on TACC? -- Big Picture***

TACC (Texas Advanced Computing Center) provides the **high-performance computing (HPC)** resources that DesignSafe uses to run jobs. Specifically, jobs submitted from DesignSafe are executed on TACC's systems — typically Stampede3 or similar clusters.


Step-by-step Process:

1. **Log into DesignSafe**
    - You access it through https://www.designsafe-ci.org
    - You don’t need to interact with TACC directly unless you want to.

1. **Use the Workspace**
    - DesignSafe has an interactive workspace:
        - Jupyter Notebooks
        - MATLAB
        - SimCenter tools
        - Other scientific apps like OpenSees, ADCIRC, etc.
    - These are all powered on the backend by TACC resources.

1. **Submit Job**
    When you submit a job via DesignSafe:
    - The job is packaged with:
        - Your script
        - Input data
        - Parameters (like CPU cores, memory, wall time)
    - DesignSafe translates this into a SLURM job (TACC uses SLURM as its job scheduler).
    - The job is then sent to a TACC queue (often the designsafe or community queue on Stampede3).

1. **Execution on TACC**
    - TACC runs the job exactly like any HPC job using SLURM.
    - The job runs on actual compute nodes (on Stampede3, for example).
    - Output files are saved in your DesignSafe project or data workspace.

1. **Results**
    - Once complete, results are sent back to DesignSafe automatically.
    - You can view, download, or analyze the data directly in the platform.


## **DesignSafe Apps** do all this automatically!
- Sets up SLURM job scripts for you
- Submits jobs via APIs to TACC’s scheduling system
- Manages your allocation (so you don’t have to use TACC’s sbatch, squeue, etc.)
You can access the APIs (Tapis) directly from your Python script.


or you can **manage intermediate steps yourself.**

