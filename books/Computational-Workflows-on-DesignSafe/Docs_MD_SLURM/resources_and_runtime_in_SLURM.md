# Resources & Runtime
***Resource Allocation & Runtime Behavior in SLURM: From Reservation to Execution on HPC Systems***

This section explains **where a SLURM job runs**, **what resources are reserved**, and **how those resources are actually used at runtime** on SLURM-based HPC systems such as Stampede3.

These behaviors apply to **all SLURM jobs**, regardless of whether they are submitted:

* directly with `sbatch`,
* through workflow tools (e.g., PyLauncher),
* or via higher-level platforms such as Tapis.

Understanding this model is essential for writing correct, efficient, and scalable jobs.

---

:::{dropdown} **What SLURM Reserves for a Job**

**Reservation ≠ execution**

When you submit a SLURM job, you request resources such as:

* number of nodes
* number of tasks or cores
* memory
* walltime
* queue / partition

SLURM **reserves** these resources before your job starts. Once scheduled:

* all requested nodes are allocated to your job
* no other job can use them during your walltime

However, **resource reservation alone does not determine how your application runs**.

:::

---

:::{dropdown} **Where the Job Starts Running**

**Batch scripts start on a single node**

When SLURM launches a job:

* the batch script begins execution on **one node** in the allocation
  (commonly the *first node*; often informally called *Node0*)

At this point:

* only the batch script is running
* no parallel work is happening yet

Unless your script explicitly launches parallel work:

* your application runs on that single node
* often as a single process
* possibly using multiple cores **only if the program is multi-threaded**

All other allocated nodes remain **idle but reserved**.

:::

---

:::{dropdown} **Using All Allocated Nodes**

**Parallelism is explicit**

Requesting multiple nodes **does not automatically distribute work**.

To use all allocated resources, your job must explicitly launch parallel execution, for example:

* MPI (`srun`, `mpirun`)
* SLURM job steps (`srun`)
* threaded runtimes (OpenMP, multithreaded BLAS)
* application-level parallelism (e.g., OpenSeesMP)

This behavior is identical for:

* manual SLURM jobs
* workflow-managed jobs
* platform-submitted jobs

SLURM provides the resources; **your script decides how to use them**.

:::

---

:::{dropdown} **Execution Environment on Compute Nodes**

**Compute nodes start clean**

SLURM jobs run on **compute nodes**, not on login nodes, portals, or JupyterHub servers.

Compute nodes typically start with a **minimal environment**:

* no modules loaded
* no Python environment active
* no shell state inherited from login or interactive sessions

Therefore:

> **All environment setup must occur inside the batch script (or a script it invokes).**

If something is not defined in the job script, **it does not exist at runtime**.

This design ensures:

* reproducibility
* isolation
* fair resource usage
* predictable performance

:::

---

## Key Takeaways (SLURM)

* SLURM **reserves resources first**
* Jobs start on **one node**
* Parallelism must be **explicitly launched**
* Compute-node environments are **clean by default**

Once this mental model is clear, SLURM behavior becomes predictable across all submission methods.
