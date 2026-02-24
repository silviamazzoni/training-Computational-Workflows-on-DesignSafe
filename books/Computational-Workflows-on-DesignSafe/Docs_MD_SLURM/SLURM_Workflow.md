# SLURM-Job Workflow
In this section we explain the workflow from **two complementary perspectives**:

1. **Platform-level view** — what happens when you submit a job from DesignSafe
2. **Scheduler-level view** — how SLURM actually queues, schedules, and runs the job

**Where Job Submission Happens**

SLURM job submission commands (such as sbatch) are issued from a login or submission node, not from compute nodes.
When using DesignSafe, this step is handled automatically for you. When working directly on a TACC system, you typically access a login node via SSH to prepare files and submit jobs.
A dedicated section later in this book covers job submission environments and workflows in detail.


## 1. Platform-level view: SLURM-Job Submission Workflow
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
  

## 1. Scheduler-level view: SLURM-Job Submission Workflow
***How does SLURM manage your job***

1. **Job Submission**

You submit a job with a **job script** that specifies:

- Number of nodes and cores (e.g., *32 cores on 4 nodes* -- *--ntasks=32*, *--nodes=4*)
- Maximum runtime (e.g., *4 hours* -- *--time=04:00:00*)
- Memory requirements (e.g., *--mem=16G*)
- Partition (queue) to submit to (**NODE TYPE** -- *--partition=skx*)
- Allocation (**project**)
- Submit with: *sbatch job_script.sh*

1. **Job Enters the Queue**
- Your job enters the **SLURM queue** and is assigned a **priority**.
- You can **monitor the queue status** using SLURM commands (e.g., *squeue*, *sacct*, etc.)


1. **SLURM Schedules the Job**
SLURM decides when and where to run your job based on:

- **Requested resources**: Number of nodes, memory, and runtime.
- **Queue priority**: System policies may prioritize shorter/smaller jobs.
- **Current system load**: Jobs may wait until required nodes become free.

1. **Job Execution**
- Once sufficient resources are available, **SLURM starts the job**.
- Your job runs on the assigned compute nodes for the allocated time.

1. **Job Completion**
When the job finishes:

- **Output files** and **logs** (e.g., *SLURM-<jobID>.out*) are generated.
- You can **check results and performance**.
