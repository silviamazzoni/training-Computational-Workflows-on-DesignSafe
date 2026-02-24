# HPC on TACC for OpenSees
***Scaling OpenSees Analyses Beyond Interactive and Single-Node Limits***

DesignSafe computations are powered by the **Texas Advanced Computing Center (TACC)**, which hosts leadership-class HPC systems such as **Stampede3**, **Frontera**, and **Lonestar6**.

For OpenSees users, HPC represents the environment where:

* models become **too large for a single machine**,
* analyses become **too slow to run interactively**, or
* the **number of simulations** becomes the dominant challenge.

HPC is therefore best understood as the **production execution environment** for OpenSees—not the place where most models are first written.

---

## What Makes HPC Different for OpenSees?

HPC systems differ from VMs and JupyterHub in one fundamental way:
**you explicitly request and control computational resources.**

This matters for OpenSees because performance is governed by:

* **Model size and sparsity**
* **Solver and numbering strategy**
* **Memory footprint of recorders**
* **Parallelization strategy (or lack thereof)**

HPC gives you access to:

* Many cores per node (shared memory)
* Many nodes per job (distributed memory via MPI)
* High-performance file systems
* Long wall-clock limits

But **HPC will not automatically make a poorly configured OpenSees model faster**—understanding how OpenSees uses resources is essential.

---

## OpenSees Execution Modes on HPC

OpenSees can be used on HPC in several fundamentally different ways.

### 1. Serial OpenSees (Single Process)

**Typical tools**

* OpenSees
* OpenSeesPy (single process)

**Best for**

* Small–moderate models
* Model verification
* Debugging
* Deterministic nonlinear analyses

**Why use HPC anyway?**

* Larger memory than laptops
* Stable long runtimes
* Batch execution of many cases

> Many “HPC” OpenSees jobs are intentionally serial. The benefit comes from *capacity*, not parallelism.

---

### 2. Shared-Memory Parallelism (Single Node, Many Cores)

**Typical tools**

* OpenSeesMP on a single node
* Threaded linear algebra libraries
* Python-level multiprocessing for ensembles

**Best for**

* Medium to large 3D models
* Faster matrix assembly and factorization
* Avoiding MPI communication overhead

This is often the **sweet spot** for OpenSees performance.

---

### 3. Distributed-Memory Parallelism (Multi-Node, MPI)

**Typical tools**

* OpenSeesMP with MPI

**Best for**

* Very large FE models
* Domain-decomposed analyses
* Research-scale simulations

**Tradeoffs**

* Communication overhead can dominate
* Requires careful tuning
* Not all OpenSees models scale well

> Multi-node OpenSeesMP is powerful—but only when the model structure justifies it.

---

### 4. Ensemble & Parametric Studies (Embarrassingly Parallel)

**Typical tools**

* OpenSeesSP
* OpenSeesPy
* Python job orchestration
* Tapis array jobs

**Best for**

* Ground-motion suites
* Fragility and risk analysis
* Sensitivity and uncertainty studies

This is **the most common and effective use of HPC for OpenSees**.

---

## Common OpenSees Analysis Types on HPC

| Analysis Type             | HPC Benefit                     |
| ------------------------- | ------------------------------- |
| Nonlinear static pushover | Larger models, batch execution  |
| Nonlinear time history    | Long runtimes, memory stability |
| Ground-motion suites      | Massive concurrency             |
| Parameter sweeps          | Automated parallel execution    |
| Fragility / risk analysis | Thousands of realizations       |
| Large 3D FE models        | Memory and solver capacity      |

---

## Choosing the Right Computational Environment

### VM vs JupyterHub vs HPC (OpenSees Perspective)

| Feature                 | VM | JupyterHub | HPC |
| ----------------------- | -- | ---------- | --- |
| Interactive development | ✅  | ✅          | ❌   |
| Easy visualization      | ✅  | ✅          | ❌   |
| Large memory            | ❌  | ⚠️         | ✅   |
| Long runtimes           | ❌  | ⚠️         | ✅   |
| Many parallel jobs      | ❌  | ⚠️         | ✅   |
| MPI scaling             | ❌  | ❌          | ✅   |
| Production runs         | ❌  | ❌          | ✅   |

**Rule of thumb**

> *Write and test in JupyterHub or a VM.
> Run at scale on HPC.*

---

## Common OpenSees HPC Pitfalls

### 1. Treating HPC Like a Bigger Laptop

* Over-requesting cores
* Under-requesting memory
* Ignoring I/O costs

### 2. Overusing MPI

* Small models do not benefit
* Communication can dominate runtime
* Debugging becomes harder

### 3. Recorder Explosion

* Too many output files
* Writing every time step unnecessarily
* Filling scratch space unintentionally

### 4. Skipping Interactive Testing

* Submitting broken scripts to the queue
* Wasting allocation time

### 5. Poor Data Movement Strategy

* Writing large outputs to slow paths
* Moving giant ZIP files unnecessarily

---

## Interactive Sessions for OpenSees Testing

TACC allows **interactive compute sessions** using `idev`:

Useful for:

* Verifying OpenSeesMP layouts
* Testing MPI counts
* Monitoring memory usage
* Diagnosing segmentation faults

This is often the **missing step** between JupyterHub testing and production HPC runs.

---

## File Staging & I/O (OpenSees-Specific)

OpenSees jobs:

* Run from **WORK or SCRATCH**
* Not from DesignSafe *My Data*

DesignSafe and **Tapis** manage:

* Input staging
* Execution
* Output retrieval

For OpenSees, this matters because:

* Output files are often very large
* Parallel jobs may write many files
* File system performance affects solver stability


---

## When HPC Is the Right Tool for OpenSees

Choose HPC when:

* Your model **no longer fits in memory**
* Analyses take **hours or days**
* You need **hundreds or thousands of runs**
* Results must be **reproducible and automated**

HPC is not a replacement for JupyterHub or VMs—it is the **scalable execution engine** for OpenSees once the model and workflow are mature.


