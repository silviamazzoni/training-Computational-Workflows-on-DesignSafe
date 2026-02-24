# Tapis as Automation

***Tapis as a SLURM Automation Layer: How Tapis Describes and Submits SLURM Jobs***

This section explains **what Tapis adds on top of SLURM**.

Tapis does **not** change:

* how SLURM allocates resources,
* where jobs run,
* or how execution behaves at runtime.

Instead, Tapis automates the **login-node orchestration** required to submit standard SLURM batch jobs.

---

## What Tapis Is (and Is Not)

* ✅ **Is**: a job-submission, staging, and monitoring layer
* ❌ **Is not**: a scheduler, executor, or alternative runtime

From SLURM’s perspective, a Tapis job is **indistinguishable** from a manually submitted batch job.

---

:::{dropdown} **How Tapis Describes SLURM Resources**

**Job attributes → scheduler requests**

When submitting a job through Tapis, resource requirements are specified in either:

* the **app definition**, or
* the **job submission request** (overrides)

Typical Tapis fields include:

* `nodeCount` – number of compute nodes
* `coresPerNode` – CPU cores per node
* `memoryMB` – memory per node
* `maxMinutes` – walltime limit
* queue name (e.g., `normal`, `development`)

These fields describe **exactly the same resources** you would request in a manual SLURM job.

Tapis does not invent new resource concepts — it mirrors SLURM’s model.

:::

---

:::{dropdown} **How Tapis Becomes a SLURM Job**

**Translation to `#SBATCH` directives**

Tapis converts job attributes into a standard SLURM batch script (`tapisjob.sh`) containing directives such as:

```bash
#SBATCH -N <nodeCount>
#SBATCH -n <total_tasks>
#SBATCH -t <walltime>
#SBATCH --mem=<memory>
```

By the time `sbatch` is invoked:

> SLURM sees the job **exactly as if you had written the batch script yourself**.

There is no special execution mode, wrapper scheduler, or bypass mechanism.

:::

---

:::{dropdown} **How Tapis Submits the Job**

**Automated login-node orchestration**

For a Tapis job submitted to a SLURM-backed system:

1. Tapis opens an SSH session to a **login node**
2. Creates the job execution directory
3. Stages input files
4. Writes the SLURM batch script (`tapisjob.sh`)
5. Runs `sbatch tapisjob.sh` on the login node

All of these actions are **lightweight orchestration tasks** — exactly what login nodes are designed for.

This is the same sequence a user would perform manually.

:::

---

:::{dropdown} **What Runs on Compute Nodes**

**Pure SLURM execution**

Once `sbatch` is called:

* SLURM queues the job
* compute nodes are allocated
* `tapisjob.sh` starts running on a compute node
* it invokes `tapisjob_app.sh`
* your application executes on compute nodes

`tapisjob_app.sh` is responsible for:

* loading modules
* activating environments
* setting paths and variables
* launching serial or parallel workloads (MPI, launchers, etc.)

From this point forward, **Tapis is no longer involved in execution**.

:::

---

:::{dropdown} **Environment Setup in Tapis Jobs**

**Nothing is inherited**

Although users interact with DesignSafe via:

* the web portal
* JupyterHub
* APIs

**none of those environments execute the job**.

Compute nodes start clean, so all environment setup must occur inside `tapisjob_app.sh`, for example:

```bash
module load python/3.12.11
module load opensees
module load hdf5/1.14.4
```

If something is not defined in the job script, **it does not exist at runtime**.

This is intentional and critical for:

* reproducibility
* isolation
* predictable performance

:::

---

## Key Takeaways

* Tapis **does not alter SLURM semantics**
* Tapis generates and submits **standard SLURM batch jobs**
* Resource usage and execution follow **exactly the same rules** as manual SLURM jobs
* Tapis automates login-node workflows — nothing more, nothing less

Once SLURM fundamentals are understood, Tapis becomes a transparent automation layer rather than a black box.
