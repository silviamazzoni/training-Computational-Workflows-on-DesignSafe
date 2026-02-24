# MPI in Tapis Apps
***Scheduler-Launched vs Script-Launched MPI, Input Staging, and Wrapper Behavior***

Tapis v3 supports **multi-node MPI workloads** in two distinct but equally powerful ways. The difference is **not performance** or **capability**, but **who launches MPI** and **how your wrapper script (*tapisjob_app.sh*) is executed**.

This section unifies:

* Tapis input staging behavior
* The *isMpi* and *mpiCmd* flags
* Internal MPI execution via *ibrun* / *mpirun*
* Practical guidance for **Python**, **OpenSees**, **OpenSeesMP**, and **mpi4py**

---

## 1. One-Time Input Staging to Shared Storage (Always)

Before discussing MPI launch modes, it is critical to understand **how Tapis stages files**.

### Single Staging Model (All Jobs)

Tapis v3 **stages inputs only once** to the execution system:

* Input data (*inputDirectory*)
* ZIP runtime contents
* *tapisjob.sh*, *tapisjob.env*, *tapisjob_app.sh*

These are unpacked into **one shared working directory** (*ExecSystemExecDir*) on a **parallel filesystem** (e.g., SCRATCH or WORK).

On systems like Stampede3 at Texas Advanced Computing Center:

* The filesystem is **visible from all compute nodes**
* Every MPI rank can read/write the same files
* **No per-node file copying occurs**

**Key implication:**
MPI jobs *do not* require node-local staging. Shared storage is the design assumption.

---

## 2. The Meaning of *isMpi* in Tapis (What It Really Controls)

In a Tapis app definition (*app.json*), the *isMpi* flag controls **only one thing**:

> **Does Tapis wrap your job in an MPI launcher?**

It does **not** control:

* Node allocation
* MPI capability
* Performance
* Whether your application *can* use MPI

Those are handled entirely by **Slurm**.

---

## 3. Non-MPI Launch Mode (*isMpi: false*)

***Serial Wrapper, MPI Inside***

This is the **default** and most flexible mode.

### What Tapis Does

* Allocates multiple nodes (if requested)
* Runs:

  * *tapisjob.sh*
  * *tapisjob_app.sh*
* **Only on the first node**

This is standard Slurm behavior for a batch script without *srun/mpirun*.

### What *You* Do

Inside *tapisjob_app.sh*, you explicitly launch MPI where needed:

```bash
ibrun python3 my_mpi_script.py
ibrun OpenSeesMP model.tcl
```

Slurm then:

* Expands the MPI job across *all allocated nodes*
* Assigns ranks
* Manages communication

### Result: Hybrid Execution Model

| Layer          | Behavior                |
| -------------- | ----------------------- |
| **Tapis**      | Single-node launcher    |
| **Slurm**      | Full MPI orchestration  |
| **Filesystem** | Shared across all nodes |

This works perfectly because:

* Inputs were staged once to shared storage
* All ranks see the same directory
* No redundant data transfers occur

---

## 4. Internal MPI via Wrapper (Why This Is Often Best)

This mode is **ideal for real scientific workflows**.

### When It Shines

* Mixed serial + parallel logic
* Environment setup and validation
* Selective MPI regions
* Python + *mpi4py*
* OpenSees + OpenSeesMP
* Avoiding race conditions

### Why It’s Safe

* No “double MPI”
* No implicit wrapping
* Full Slurm context is available:

  * *SLURM_NODELIST*
  * *SLURM_NTASKS*
  * *_tapisNodes*
  * *_tapisCoresPerNode*

### Example: Script-Launched MPI (Recommended)

```json
"isMpi": false,
"mpiCmd": null
```

```bash
# Serial sanity checks
python -V

# MPI only where needed
ibrun python -m mpi4py my_analysis.py
```

This is especially important for:

* Installing or building *mpi4py*
* Writing files once
* Generating shared metadata

---

## 5. Scheduler-Launched MPI (*isMpi: true*)

***MPI From Line 1***

In this mode, **Tapis injects the MPI launcher for you**.

### What Changes

* *tapisjob_app.sh* runs on **all MPI ranks**
* You must **not** call *ibrun* or *mpirun* yourself
* *mpiCmd* must be defined

```json
"isMpi": true,
"mpiCmd": "ibrun"
```

```bash
# Already running on all ranks
python -m mpi4py your_program.py
```

### Responsibilities Shift to You

You must guard:

* File creation
* Logging
* Output summaries

```python
from mpi4py import MPI
if MPI.COMM_WORLD.rank == 0:
    write_summary()
```

### When This Mode Is Best

* Entire workflow is MPI
* Minimal serial logic
* You are already MPI-safe everywhere

---

## 6. Avoiding Double MPI (Critical Rule)

> **Either Tapis launches MPI — or you do. Never both.**

| Mode               | *isMpi* | *mpiCmd*  | Call *ibrun* yourself? |
| ------------------ | ------- | --------- | ---------------------- |
| Scheduler-launched | *true*  | *"ibrun"* | ❌                      |
| Script-launched    | *false* | *null*    | ✅                      |

**Schema tip:**
If *isMpi=false*, *mpiCmd* must be **null**, not an empty string.

---

## 7. Performance & I/O Reality Check

There is **no performance penalty** for script-launched MPI:

* Shared scratch/work filesystems are designed for this
* Avoiding per-node duplication often **reduces overhead**
* MPI scaling is identical

The difference is **control**, not speed.

---

## 8. Practical Guidance by Application Type

### OpenSeesMP

✔ Recommended:

* *isMpi: false*
* *ibrun OpenSeesMP model.tcl*

### OpenSeesPy + *mpi4py*

✔ Recommended:

* Script-launched MPI
* Guard rank-0 I/O
* Explicit *ibrun*

### Pure Python (non-MPI)

✔ Keep *isMpi=false*
✔ Request 1 node

### End-to-End MPI Codes

✔ Use *isMpi=true*
✔ No internal launcher calls

---

## 9. Mental Model Summary

> **Tapis stages once. Slurm runs parallel. You choose who starts MPI.**

* Tapis = orchestration + staging
* Slurm = scheduling + parallelism
* *tapisjob_app.sh* = your control plane

Used correctly, this model gives you:

* Full MPI scalability
* Clean I/O
* Zero redundant transfers
* No loss of capability

**You get the best of both worlds — every time.**
