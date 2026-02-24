# Execution Strategy Matrix
***Matching workload behavior to execution structure***

The table below summarizes structural differences between execution strategies, not tool-specific implementations.


| Execution Strategy          | Best-Fit Workloads                                  | Task Coupling | Resource Focus         | Typical Scaling Pattern   | Key Risks                          |
| --------------------------- | --------------------------------------------------- | ------------- | ---------------------- | ------------------------- | ---------------------------------- |
| **Embarrassingly Parallel** | Monte Carlo, parametric sweeps, batch preprocessing | Independent   | CPU, I/O               | Many small jobs           | Scheduler overhead, file explosion |
| **Single Long Batch**       | Stepwise simulations, nonlinear solvers             | Sequential    | CPU, memory            | Longer walltime           | Idle cores if poorly parallelized  |
| **Tightly Coupled MPI**     | Large FE models, domain-decomposed solvers          | Strong        | Memory, network        | Fewer larger jobs         | Communication & load imbalance     |
| **Pipeline / Multi-Stage**  | Pre → simulate → post workflows                     | Mixed         | I/O, orchestration     | Stage-by-stage            | Data movement dominates runtime    |
| **Accelerated (GPU)**       | ML training, dense linear algebra                   | Internal      | GPU memory & bandwidth | Fewer high-intensity jobs | Idle accelerators, poor staging    |

**Key takeaway:**
Scaling is not one-dimensional. A strategy that scales well in *number* may scale poorly in *size* or *communication*.

---

## Execution Strategy Decision Tree


**Step 1 — Are tasks independent?**

* **Yes** → Embarrassingly parallel
* **No** → Go to Step 2

**Step 2 — Do tasks communicate frequently?**

* **Yes** → Tightly coupled (MPI-style execution)
* **No** → Go to Step 3

**Step 3 — Is the workload long-running or staged?**

* **Single long run** → Single large batch
* **Multiple stages** → Pipeline / multi-stage execution

**Step 4 — Is compute dominated by matrix ops or learning loops?**

* **Yes** → Accelerated (GPU-based)
* **No** → CPU-based batch execution

This decision tree is intentionally **tool-agnostic**. The same strategy can later be implemented using different systems.

---

## Common Strategy Mistakes (and How to Avoid Them)

* **Running independent tasks as one big job**
  → wastes cores and walltime

* **Adding nodes to tightly coupled jobs without decomposition**
  → increases communication overhead

* **Using GPUs without data staging discipline**
  → accelerators sit idle

* **Over-fragmenting pipelines**
  → file transfer dominates runtime

Execution strategy is about **matching structure to behavior**, not maximizing resources.
