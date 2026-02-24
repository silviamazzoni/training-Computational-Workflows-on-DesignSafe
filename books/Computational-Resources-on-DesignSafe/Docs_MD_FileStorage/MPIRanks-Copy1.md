# MPI Ranks
***MPI ranks, nodes, and scratch space: what you need to know first***

Before using node-local `/tmp` storage safely in an MPI job, it is important to understand **how parallel processes are organized and identified** at runtime. The file-management patterns that follow rely on these concepts to avoid file collisions, race conditions, and data loss.

This section introduces the core MPI and Slurm concepts you will see referenced throughout the storage chapter.

---

### What is an MPI *rank*?

In an MPI job, your program is launched **multiple times** in parallel.
Each running instance is called a **rank**.

* Every rank executes the *same program*
* Each rank has a **unique integer ID**
* Ranks typically cooperate by exchanging data via MPI

The rank ID is commonly referred to as:

```text
MPI rank  (0, 1, 2, ..., N−1)
```

In Slurm-launched jobs (including Tapis jobs on TACC systems), this value is exposed as:

```bash
SLURM_PROCID
```

Example:

* `SLURM_PROCID=0` → rank 0 (often used for coordination or aggregation)
* `SLURM_PROCID=7` → the 8th MPI process

When writing files, **two ranks with the same filename will overwrite each other unless separated**. This is why rank-aware paths are essential.

---

### Nodes vs. ranks: why this distinction matters

A **node** is a physical (or virtual) machine in the cluster.

* Each node has:

  * its own CPUs
  * its own memory
  * its own `/tmp` directory
* Multiple MPI ranks typically run on **the same node**

Slurm provides two important identifiers:

| Concept    | Meaning                      | Slurm variable  |
| ---------- | ---------------------------- | --------------- |
| Rank ID    | Global MPI process index     | `SLURM_PROCID`  |
| Node ID    | Which node in the allocation | `SLURM_NODEID`  |
| Local rank | Rank index *within* a node   | `SLURM_LOCALID` |

Example:

* Rank 12 may be:

  * `SLURM_NODEID=1` (second node)
  * `SLURM_LOCALID=4` (5th rank on that node)

This matters because **all ranks on the same node share the same `/tmp` directory**.

---

### Why `/tmp` requires special handling in MPI jobs

The `/tmp` directory is:

* **Fast** (node-local disk or RAM-backed)
* **Not shared across nodes**
* **Shared by all ranks on the same node**
* **Deleted when the job ends**

As a result:

* `/tmp/input.dat` is visible to *all ranks on that node*
* Rank collisions will occur unless filenames or directories are separated
* Files in `/tmp` must be explicitly copied back to shared storage

This is fundamentally different from Tapis-staged directories on shared filesystems, where all nodes see the same paths.

---

### Common environment variables used in this chapter

These variables are automatically defined by Slurm (and therefore by Tapis on Slurm systems):

| Variable            | Description                          |
| ------------------- | ------------------------------------ |
| `SLURM_PROCID`      | Global MPI rank ID                   |
| `SLURM_LOCALID`     | Rank index within a node             |
| `SLURM_NODEID`      | Node index within the job allocation |
| `SLURM_JOB_ID`      | Scheduler job identifier             |
| `USER`              | Unix username                        |
| `TAPIS_JOB_WORKDIR` | Shared job execution directory       |

Throughout this chapter, these variables are used to:

* create unique per-rank or per-node directories
* coordinate file copies safely
* control cleanup behavior

---

### Why rank-aware file management is essential

Without rank-aware file paths:

* ranks overwrite each other’s temporary files
* partial files are read before being fully written
* jobs fail intermittently and are difficult to debug

By explicitly separating files by **rank** and **node**, you gain:

* deterministic behavior
* reproducibility
* safe use of high-performance node-local storage

---

### How this fits into the broader storage model

In summary:

* **Shared filesystems** (e.g., Work, Scratch):

  * single job directory
  * visible to all nodes
  * ideal for inputs and final outputs

* **Node-local `/tmp`**:

  * fast but ephemeral
  * requires explicit management
  * ideal for temporary, I/O-intensive data

The MPI-safe patterns that follow build directly on these concepts and show how to combine **correctness** and **performance** in large-scale parallel workflows.
