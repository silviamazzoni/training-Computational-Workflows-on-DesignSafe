# Tapis-Job Profiling
***Profiling Job State Durations to Improve Efficiency***

By tracking how long a job spends in **each stage of its lifecycle** (such as *PENDING*, *QUEUED*, *RUNNING*, *STAGING_INPUTS*, and *ARCHIVING*), users can **identify performance bottlenecks** and inefficiencies in their workflow. This process is known as **job profiling**.

A key point—often overlooked—is that **a significant fraction of total job time may be spent *outside* the RUNNING phase**, particularly during **file transfers at the beginning and end of a Tapis job**.

### Interpreting Job States

Some common patterns you may observe:

* **Long time in *PENDING* or *QUEUED***
  → Requested resources may be too large, or the queue may be heavily loaded.

* **Fast *RUNNING* but slow *ARCHIVING***
  → Your workflow is likely producing too many files or very large outputs.

* **Delays before the job starts running**
  → Input file staging (uploads, copies, or decompression) may be the bottleneck.

* **Immediate *FAILED***
  → Often points to missing input files, incorrect paths, environment setup issues, or permissions problems.

Profiling allows you to:

* Optimize resource requests (cores, memory, wall time)
* Select more appropriate queues or systems
* Refactor I/O-heavy scripts
* Understand non-compute overhead (input staging, archiving, metadata operations)

> **The goal is not just to make jobs run — but to make them scale efficiently and predictably.**

---

## Why File-Transfer Stages Matter (A Lot)

In many Tapis workflows, **file transfers dominate wall-clock time**, especially when jobs:

* Move **large numbers of small files**
* Repeatedly transfer the **same common inputs**
* Write extensive intermediate outputs that are later archived

Tapis is extremely powerful for automation and reproducibility, but **it is not optimized for moving thousands of individual files**. Every file transfer involves metadata operations, authentication, and filesystem overhead.

### Best Practices for Managing File Transfers

:::{dropdown} **1. Minimize the number of transferred files**
Prefer:

* Fewer, larger files
* Structured directories over flat folders with many files

Avoid:

* Thousands of small text or CSV files
* Repeatedly transferring the same static inputs

:::

:::{dropdown} **2. Keep common inputs in *Work* or scratch storage**

For shared or reusable inputs (e.g., ground-motion sets, large mesh files, lookup tables):

* Store them **once** in your *Work* directory or system scratch
* Reference them directly from your job script instead of re-uploading

⚠️ **Important:**
Scratch and *Work* spaces may be cleaned periodically. You are responsible for:

* Verifying files exist before running
* Re-populating them when needed
* Treating scratch as *performance space*, not archival storage

:::

:::{dropdown} **3. Stage results strategically**

Instead of archiving everything at the end:

* Write **intermediate or temporary files** to *Work* or scratch during the run
* Archive **only final or essential outputs**
* Perform aggregation or post-processing *before* archiving

This is especially effective now that ***Work* is accessible from Jupyter**, enabling you to:

* Inspect results interactively
* Run post-processing notebooks
* Collect or compress outputs *after* the job finishes

:::

:::{dropdown} **4. Use ZIP files intentionally**

Zipped files can dramatically reduce transfer overhead:

* **Inputs**:
  Upload a single ZIP file → unzip inside your job script

* **Outputs**:
  Package results into one or a few ZIP files → archive those instead of thousands of files
:::


This approach:

* Reduces file-count overhead
* Speeds up both staging and archiving
* Improves reproducibility

:::{dropdown} **Sample I/O checklist**

**I/O checklist before you submit a Tapis job**

1. **Profile the full lifecycle**

* [ ] Did you look at **STAGING_INPUTS** and **ARCHIVING**, not just RUNNING?
* [ ] Are you tracking totals across multiple jobs to see what’s “normal” for your workflow?

1. **Reduce file count (this is usually #1)**

* [ ] Can you replace “many small files” with **fewer larger files**?
* [ ] Can outputs be aggregated (one CSV/HDF5/JSON per job rather than thousands)?

1. **Handle common inputs intelligently**

* [ ] Are shared inputs (e.g., ground motions) stored once in **Work/scratch** instead of re-staged every run?
* [ ] Do you have a simple **“existence check”** step so jobs fail fast if scratch was cleaned?
* [ ] Do you have a plan to periodically **refresh** scratch if it’s purged?

1. **Stage outputs strategically**

* [ ] Are you writing bulky intermediates to **Work/scratch** during RUNNING?
* [ ] Are you archiving only **final** / **essential** deliverables?
* [ ] Are you planning to collect/post-process afterwards in **Jupyter (since Work is accessible)**?

1. **Use ZIPs on purpose**

* [ ] Do you ZIP inputs (configs, tables, many small files) and unzip on the compute node?
* [ ] Do you ZIP outputs (or chunk into multiple ZIPs if very large) before archiving?

1. **Sanity checks**

* [ ] Did you request reasonable wall time so the job doesn’t get killed mid-run (wasting staging cost)?
* [ ] Are logs (stdout/stderr) small and readable (so debugging doesn’t require downloading huge trees)?

:::
