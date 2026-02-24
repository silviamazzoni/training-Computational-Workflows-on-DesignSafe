# Filesystems in SLURM
***Shared Files vs. Node-Local Temporary Storage***

Just as you would do for a manual SLURM job, Tapis stages all inputs into a **single job directory** on a shared filesystem (for example, */scratch* or */work2*). Because TACC systems use **parallel shared filesystems**:

* Every compute node can see the same staged files
* Inputs are **not copied separately** to each node
* Multi-node jobs simply access the same directory

This behavior is fundamental to MPI-based workflows (including OpenSeesMP), where all ranks must have consistent access to the same inputs and outputs.

---

### Using Node-Local */tmp* on Execution Nodes

In addition to the shared filesystem, **each compute node also provides fast, node-local temporary storage**, typically mounted at */tmp*. This storage is physically attached to the node and is **not shared** across nodes.

#### Why use */tmp*?

Node-local storage is often:

* **Much faster** for read/write operations
* Free from shared-filesystem contention
* Ideal for **temporary, high-I/O workloads**

Typical use cases include:

* Scratch files created repeatedly inside tight loops
* Intermediate outputs that do not need to persist
* Temporary databases, caches, or solver working files
* Per-rank scratch files in MPI jobs

For I/O-intensive analyses, copying selected files to */tmp* can significantly reduce runtime.

---

### How it Works in Practice

Because */tmp* is **node-local**, files must be explicitly managed:

1. **Copy inputs from the shared job directory to */tmp***

   ```bash
   cp input.dat /tmp/input.dat
   ```

2. **Run your analysis using */tmp* paths**

   ```bash
   ./solver /tmp/input.dat
   ```

3. **Copy required outputs back to the shared filesystem**

   ```bash
   cp /tmp/output.dat $TAPIS_JOB_WORKDIR/
   ```

Each MPI rank may do this independently, or rank 0 may manage shared files depending on your workflow.

---

### Important Trade-Offs

Using */tmp* improves performance **at a cost**:

**Advantages**

* Faster I/O
* Reduced pressure on shared filesystems
* Better scalability for I/O-heavy workloads

**Costs**

* Files are **not persistent** (deleted when the job ends)
* Files must be **manually copied in and out**
* More complex job scripts
* Risk of data loss if outputs are not explicitly saved

Because of this, **only temporary files should ever be written to */tmp***. All final outputs, logs, and results must be copied back to the shared filesystem before the job exits.

---

### Best-Practice Guidance

* Use shared filesystems for:

  * Inputs
  * Final outputs
  * Logs and checkpoints

* Use */tmp* for:

  * Short-lived scratch data
  * High-frequency I/O
  * Intermediate solver files

* Always:

  * Cleanly manage file copies
  * Assume */tmp* is empty at job start and destroyed at job end

---

### Key Takeaway

Tapis stages inputs once on a shared filesystem for correctness, reproducibility, and simplicity.
**Advanced users can selectively leverage node-local */tmp* for performance**, but doing so requires explicit file management and discipline.

Used carefully, this approach can deliver substantial speedups—used indiscriminately, it can create fragile and hard-to-debug workflows.

