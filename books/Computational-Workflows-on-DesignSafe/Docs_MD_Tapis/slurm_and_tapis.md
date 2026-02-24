# SLURM and Tapis
***From Scheduler Mechanics to Automated Workflows***

At this point, you already understand how **SLURM** works directly: you request resources, submit a batch script, wait in a queue, run on allocated nodes, and collect outputs. What changes when you use **Tapis** is **not** how jobs run — it’s *how workflows are described, launched, managed, and reused*.

**Tapis does not replace SLURM.**
It **orchestrates** SLURM.

Think of Tapis as a **translation and management layer** that converts higher-level job descriptions into the same SLURM mechanics you already know, then tracks, stages, archives, and exposes everything programmatically.

---

## The conceptual shift: *Scripts → Descriptions*

When working directly with SLURM, the batch script is both the **definition of the workflow** and the **mechanism for running it**. With Tapis, those responsibilities are deliberately separated.

| If you were using SLURM directly  | With Tapis                            |
| --------------------------------- | ------------------------------------- |
| Write and edit an `sbatch` script | Define a **Tapis App** once           |
| Modify scripts per run            | Submit **Tapis Jobs** with parameters |
| Manually stage inputs             | Tapis stages inputs automatically     |
| Monitor with `squeue` / `sacct`   | Query job state via API, CLI, Python  |
| Track outputs yourself            | Tapis archives outputs + metadata     |

You still request the **same resources** — nodes, cores, walltime, queues — but you express them **declaratively**, rather than embedding them repeatedly in scripts.

A helpful way to think about it:

> A **Tapis App** captures what used to live in a SLURM script.
> A **Tapis Job** captures what used to change from run to run.

---

## SLURM concepts vs. Tapis concepts (mental mapping)

This mapping is the key to demystifying Tapis. Nothing here is new — it’s simply reorganized.

| SLURM concept             | What it controls             | Tapis equivalent           |
| ------------------------- | ---------------------------- | -------------------------- |
| Batch script (`sbatch`)   | Execution logic + directives | **Tapis App**              |
| Job submission (`sbatch`) | Send job to scheduler        | **Tapis Job submission**   |
| Partition / queue         | Priority & limits            | `execSystemLogicalQueue`   |
| Nodes                     | Physical machines            | `nodeCount`                |
| Tasks / cores             | Parallelism                  | `coresPerNode`, MPI config |
| Walltime                  | Max runtime                  | `maxMinutes`               |
| Working directory         | Runtime location             | Tapis execution directory  |
| Stdout / stderr           | Logs                         | Archived job logs          |

Once you see this correspondence, Tapis stops feeling “magical” and starts feeling like a **well-organized automation of SLURM**.

---

## What SLURM controls (and always will)

SLURM remains the **scheduler of record**. It is responsible for:

* allocating nodes, cores, and memory
* queuing jobs and enforcing priorities
* launching MPI, serial, and hybrid workloads
* tracking job states (*PENDING*, *RUNNING*, *COMPLETED*, *FAILED*)

If you write SLURM scripts directly, **you control everything** — resource flags, execution commands, file paths, scratch usage, arrays, and dependencies. This offers maximum flexibility, but also maximum responsibility.

For many users, **direct SLURM scripts are the prototype**: they are how you understand performance, scaling, and failure modes before automating anything.

---

## What Tapis adds on top of SLURM

Tapis sits *above* the scheduler and automates the **surrounding workflow**:

* input staging (MyData, Projects, Work, external systems)
* output collection and archiving
* job submission and monitoring
* consistent execution environments
* programmatic access (API, Python, CLI, Web Portal)

When you submit a Tapis job, SLURM still runs it on systems at the Texas Advanced Computing Center — for example on Stampede3 — but you no longer have to manage all of the *glue* yourself.

Tapis automates the mechanics **without hiding the truth**:

* jobs still wait in queues
* resource limits still apply
* walltime is still enforced
* MPI and threading behave exactly the same

The difference is **where intent is expressed**.

---

## When direct SLURM makes sense

Using SLURM directly is often the right choice when:

* developing or debugging low-level performance behavior
* experimenting interactively on the cluster
* using advanced scheduler features (complex arrays, dependencies)
* building short-lived or highly customized workflows

In these cases, working close to the scheduler is an advantage.

---

## When Tapis automation makes sense

Tapis becomes essential when workflows need to be:

* **repeatable** — same run, different inputs
* **scalable** — many jobs, many users, many datasets
* **shareable** — others can run without reading your scripts
* **integrated** — Web Portal, Jupyter, Python, CLI all behave consistently

This is especially important for:

* ensemble studies
* uncertainty quantification
* parameter sweeps
* production runs
* teaching and training materials

---

## A healthy mental model

A concise way to hold all of this together:

> **SLURM defines how jobs run.**
> **Tapis defines how workflows are launched, managed, and reused.**

You don’t replace SLURM by learning Tapis.
You **encapsulate** SLURM inside a more robust workflow system.

---

## The developer bridge

For app authors and advanced users, Tapis is best understood as a **programmatic SLURM job generator**:

* Tapis generates scheduler-facing scripts (e.g., `tapisjob.sh`)
* It exports parameters and paths via environment files (e.g., `tapisjob.env`)
* It submits the job with `sbatch`
* It monitors scheduler state and maps it into Tapis job states
* It invokes **your app wrapper** (commonly `tapisjob_app.sh`) on the compute nodes
* It archives outputs and preserves logs and metadata

All of this happens using the **same SLURM mechanisms** you would use manually — just assembled, executed, and tracked automatically.

The detailed timing, file-transfer stages, login-node vs compute-node behavior, and performance implications are covered in the **in-depth Tapis execution sections that follow**, so they are not repeated here.

---

## A common (and recommended) progression

Most advanced users naturally evolve along this path:

1. Run jobs interactively (Web Portal, JupyterHub)
2. Write SLURM scripts to understand scaling and performance
3. Wrap those scripts into Tapis Apps
4. Automate execution using Python or the CLI
5. Reuse and extend workflows across projects and collaborators

Each step builds on the previous one — nothing is discarded.

---

## Why this matters for long-term work

Research workflows change:

* models grow
* datasets expand
* collaborators rotate
* questions evolve

Separating:

* **execution mechanics** (SLURM)
* from **workflow logic** (Tapis)

is what allows your work to scale **without becoming brittle**.

That separation is what turns one-off jobs into **sustainable computational infrastructure**.
