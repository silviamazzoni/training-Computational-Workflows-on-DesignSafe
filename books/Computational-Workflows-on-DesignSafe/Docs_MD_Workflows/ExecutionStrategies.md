# Execution Strategies
***How workloads are mapped onto compute systems***

An **execution strategy** describes *how* a workload is launched, distributed, coordinated, and completed on a computing system. While the **workload** defines computational behavior, the **execution strategy** defines **control flow**, **parallel structure**, and **resource usage**.

Crucially, **execution strategies are independent of tools**. The same strategy may be implemented using JupyterHub, SLURM scripts, or Tapis apps — what changes is *automation*, not intent.


---

## Why Execution Strategies Matter

Execution strategies sit **between scientific intent and computing tools**.

They answer questions such as:

* Should tasks run **independently or in coordination**?
* Should the workflow be **one long job** or **many small jobs**?
* Is performance limited by **CPU, memory, communication, or I/O**?
* Does scaling mean **more tasks**, **larger tasks**, or **longer runs**?

Understanding execution strategies prevents common pitfalls such as:

* oversubscribing memory,
* underutilizing nodes,
* overwhelming the filesystem with small files,
* or adding resources that *reduce* performance.

  
---

## The Three Core Execution Dimensions

Every execution strategy is shaped by how a workload behaves along three fundamental dimensions:

:::{Dropdown} 1. Task Independence

Do individual tasks depend on each other?

* **Independent tasks** → can run in any order or in parallel
  *(Monte Carlo, parameter sweeps)*
* **Dependent tasks** → must run in sequence or coordinated steps
  *(time-marching simulations, multi-stage workflows)*

:::

:::{Dropdown} 2. Resource Coupling

Do tasks share memory or communicate frequently?

* **Loosely coupled** → minimal communication, file-based exchange
* **Tightly coupled** → frequent synchronization, shared state, MPI

:::

:::{Dropdown} 3. Time Structure

How does the workload evolve over time?

* **Short-lived tasks** → many fast jobs, scheduling overhead matters
* **Long-running tasks** → stability, checkpointing, and walltime matter
* **Iterative tasks** → repeated execution with evolving state

:::

These dimensions—not the software—determine the correct execution strategy.

Importantly, a single workflow may change execution strategy over its lifetime — for example, starting as embarrassingly parallel during exploration and evolving into a tightly coupled execution at scale.

---

### Common Execution Strategies

Below are the most common execution strategies used on DesignSafe and similar HPC platforms.

:::{Dropdown} 1. Embarrassingly Parallel Execution

**Best for:** Monte Carlo, parameter sweeps, batch preprocessing

* Each task runs independently
* Minimal memory per task
* Scales horizontally across many cores or nodes

**Typical patterns:**

* Job arrays
* Parameterized batch jobs
* Task launchers

**Key risk:** scheduling overhead and file I/O explosion

:::

:::{Dropdown} 2. Single Large Batch Execution

**Best for:** Stepwise simulations, long-running solvers

* One job runs for a long time
* Memory footprint is stable
* Parallelism is moderate or internal

**Typical patterns:**

* Single SLURM job
* Multi-core shared-memory execution
* Checkpoint/restart cycles

**Key risk:** underutilization if parallelism is limited

:::

:::{Dropdown} 3. Tightly Coupled MPI Execution

**Best for:** Large structural models, domain-decomposed simulations

* Tasks exchange data frequently
* Strong synchronization requirements
* Memory and network performance dominate

**Typical patterns:**

* MPI ranks per node
* Domain decomposition
* Collective communication

**Key risk:** communication overhead and load imbalance

:::

:::{Dropdown} 4. Pipeline / Multi-Stage Execution

**Best for:** Preprocess → simulate → postprocess workflows

* Workload is decomposed into stages
* Each stage may use a different execution strategy
* Intermediate data must be staged carefully

**Typical patterns:**

* Sequential job chaining
* Workflow managers
* Conditional execution

**Key risk:** data movement dominates runtime

:::

:::{Dropdown} 5. Accelerated Execution (GPU / Specialized Hardware)

**Best for:** ML training, large matrix operations, some preprocessing

* High compute intensity
* Performance sensitive to memory layout and data transfer
* Often paired with CPU preprocessing

**Typical patterns:**

* GPU-enabled batch jobs
* Hybrid CPU/GPU pipelines

**Key risk:** idle accelerators due to poor data staging

:::

---

## Execution Strategy ≠ Platform

A critical distinction:

> **Execution strategies describe structure — not tools.**

The same strategy can be implemented using:

* JupyterHub (interactive, exploratory)
* SLURM batch scripts (manual control)
* Tapis apps (automated, repeatable workflows)

The *strategy* stays the same; only the **level of automation and orchestration** changes.

---

## Execution Strategy ≠ Resource Size

A critical misconception is that **scaling a workload means adding more resources**.

> Many workloads fail to scale because the *execution strategy* does not match the *workload structure*.

Examples:

* Adding nodes to a tightly coupled simulation may **slow it down**
* Running many tiny tasks as one job may **waste cores**
* GPU jobs without sufficient preprocessing may **idle accelerators**

Choosing the right execution strategy is often more important than choosing the largest system.


---

## Looking Ahead

In later chapters, these execution strategies will be mapped to:

* Interactive environments (e.g., JupyterHub)
* Batch systems (SLURM)
* Automated pipelines (Tapis applications)

The goal is not to lock you into a single approach, but to give you a **strategy-first mindset** for building scalable, reusable computational workflows.


---

## Guiding Principle

> **Performance problems are usually strategy problems, not hardware problems.**
