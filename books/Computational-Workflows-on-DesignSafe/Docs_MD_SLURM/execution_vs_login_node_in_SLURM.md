# Login vs Execution Nodes
***Login Nodes vs Execution Nodes in SLURM: Where Commands Run on HPC Systems***

Understanding **where commands execute** is fundamental when working on SLURM-based HPC systems such as Stampede3.

Confusion between **login nodes** and **compute (execution) nodes** is one of the most common sources of misunderstanding in HPC—and SLURM enforces this distinction strictly.

At a high level:

* **Login nodes** are for *interaction and orchestration*
* **Compute nodes** are for *actual computation*
* **SLURM always enforces this separation**

This model applies to **all SLURM jobs**, regardless of how they are submitted.

---

:::{dropdown} **Login Nodes**

**Where orchestration happens**

Login nodes are intended for:

* editing files
* preparing job scripts
* submitting jobs
* lightweight inspection and setup

They are **not** intended for heavy computation.

Key points:

* `sbatch` runs on the **login node**
* no SLURM jobs execute on login nodes
* CPU- or memory-intensive work is prohibited

Login nodes exist to protect the stability of the shared system.

:::

---

:::{dropdown} **Compute (Execution) Nodes**

**Where computation happens**

All SLURM jobs execute on **compute nodes**:

* batch scripts start here
* applications run here
* MPI ranks and threads run here

When a job is scheduled:

* SLURM allocates compute nodes
* the batch script is launched on one node in the allocation
* all actual computation occurs on compute nodes only

Login nodes are never involved once execution begins.

:::

---

:::{dropdown} **What `sbatch` Actually Does**

**Submission vs execution**

A common misconception is that `sbatch` *runs* a job.

In reality:

* `sbatch` submits a job **to SLURM**
* SLURM queues the job
* when resources become available, SLURM launches the batch script on compute nodes

Important clarification:

> **`sbatch` always runs on a login node.
> Batch scripts never do.**

This distinction is fundamental to how SLURM operates.

:::

---

## Key Takeaways

* Login nodes orchestrate
* Compute nodes execute
* `sbatch` runs on login nodes
* Batch scripts and applications run on compute nodes
* This model is always enforced by SLURM

Once this mental model is clear, many HPC behaviors become immediately predictable.
