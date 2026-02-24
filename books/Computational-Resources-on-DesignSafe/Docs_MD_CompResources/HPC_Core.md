# Cores
***Cores allow computers to process multiple tasks simultaneously, increasing speed and efficiency.***

**Cores** are a fundamental part of modern **CPU (Central Processing Unit)** and GPU **(Graphics Processing Unit)** architecture.

- A **core** is a **processing unit** within a CPU or GPU that can execute instructions independently. Think of a core as a mini-processor inside the **main processor**.
- In the early days of computing, CPUs had a **single core** that handled all tasks sequentially.
- Modern processors have **multiple cores**, allowing them to handle multiple tasks simultaneously, which is known as **parallel processing**.



Running one process per core may seem efficient—but if each process is memory-hungry, they will **compete for RAM**, leading to:

    * **Slower performance**
    * **Crashes or segmentation faults**
    * **Paging or swapping**, which dramatically degrades I/O speed
If your simulation needs more memory than what’s available per core, consider **running fewer processes per node** to give each one more memory and improve performance and stability. This is particularly important when launching large MPI jobs or using solvers like OpenSeesSP that allocate large memory blocks.


## Single vs Multi-Core Processes

Analogy: Workers in a Kitchen
- Imagine a kitchen where you have tasks to complete, like chopping vegetables, boiling water, and baking.
- A **single-core processor** is like having one chef who does everything one task at a time.
- A **multi-core processor** is like having multiple chefs working on different tasks simultaneously, making the kitchen more efficient.

## Multi-Processing vs Multi-Threading

In the context of HPC systems like **Stampede3 at TACC**, it’s important to distinguish between **multi-processing** and **multi-threading**, as this impacts how your code should be designed and how resources are requested.

* **Multi-Processing**

    * **Multi-processing** involves running **multiple separate processes**, each with its **own memory space**.
    * This model is well-suited to HPC environments and **fully supported on TACC** systems.
    * Most parallel jobs on Stampede3 use **MPI (Message Passing Interface)**, which is a multi-processing model.
    * Each **process is typically assigned to a single core**.
    
      * On Stampede3, users commonly run **one MPI process per physical core**.
      * For example, if a node has 128 cores, you can run **up to 128 MPI processes** on that node.

* **Multi-Threading**

    * **Multi-threading** allows a **single process** to create multiple threads that share memory and can run tasks concurrently.
    * This model uses **shared memory**, and threads are generally more lightweight than processes.
    * Examples include **OpenMP** programs.

## TACC Policy and Best Practices

* On Stampede3, **multi-threading is technically supported**, but **not enabled by default** in most queued environments.
* **The default execution model is one process per core.**
* If you want to use **multi-threading (e.g., OpenMP)**, you need to explicitly:

  * **Set the number of threads** (e.g., via the `OMP_NUM_THREADS` environment variable).
  * **Request fewer MPI processes** to avoid oversubscribing cores.
  * **Ensure your job script and module environment support hybrid MPI + OpenMP execution.**

## Can You Run Multiple Processes per Core?

* While technically possible (via over-subscription), **running more than one process per core is strongly discouraged** on TACC systems.
* Doing so can degrade performance due to context switching and resource contention.
* The standard and recommended practice is: **one process per core, unless using multi-threading**.

Here’s a clear **table** to visually summarize **Multi-Processing vs Multi-Threading** on Stampede3 at TACC:


## HPC Parallel Execution Models

| Feature              | **Multi-Processing (MPI)**            | **Multi-Threading (OpenMP)**                     |
| -------------------- | ------------------------------------- | ------------------------------------------------ |
| **Model Type**       | Separate processes                    | Shared-memory threads                            |
| **Common Usage**     | ✅ Fully supported and widely used     | ⚠️ Supported but **not enabled by default**¹     |
| **Resource Binding** | 1 process per physical core           | 1 process can spawn multiple threads             |
| **Memory Space**     | Each process has its own memory space | All threads share the same memory                |
| **Setup on System**  | Default; no special setup required¹   | Must set `OMP_NUM_THREADS` and configure job¹    |
| **Efficiency**       | Good for distributed tasks            | Good for fine-grained, shared-memory parallelism |
| **Best Practice**    | Run **1 MPI process per core**¹       | Avoid oversubscribing cores¹                     |
| **Oversubscription** | ❌ Not recommended (hurts performance) | ❌ Threads > cores causes slowdowns               |


¹ **Stampede3-specific note**: On Stampede3 at TACC, the default job launch environment (e.g., `ibrun`) is configured for **1 MPI process per physical core**. Multi-threading is supported (e.g., OpenMP or hybrid MPI+OpenMP), but requires **explicit configuration** in your job script and environment. Stampede3 nodes have **128 physical cores** (2×64), and exceeding that without adjustment may result in performance degradation or job misconfiguration.


## Specifying the Number of Cores in a Job

How you specify the number of cores for your job depends on the **application** and **job submission method** you're using on **Stampede3** (and other TACC systems).

* **General Concept**

    The **total number of cores** for a job is typically computed as:
    
    > **`# of cores = # of nodes × # of cores per node`**
    
    On **Stampede3 skx** nodes have **128 physical cores**. However, how you specify and distribute those cores depends on your toolchain:

* **In SLURM Job Scripts**

    * SLURM handles resource allocation automatically.
    * You typically **specify the total number of MPI processes** (which usually equals the total number of cores).
    * SLURM will **evenly distribute the processes across all nodes** unless instructed otherwise.

* **Example:**

    ```bash
    #SBATCH -N 2               # Request 2 nodes
    #SBATCH -n 256             # Request 256 total MPI tasks (processes)
    ```
    
    → This allocates **256 cores** across **2 nodes**, using **128 cores per node**.
    
* **With PyLauncher (advanced)**

    PyLauncher gives you more **fine-grained control**:
    * You can **specify total number of cores** via the launcher configuration.
    * Or, define the **number of cores per command** in the input file (`input.in`), letting PyLauncher handle distribution.
    
    This flexibility is useful for **ensemble jobs** or **task farming**, where each command might use a different number of cores.

* **In DesignSafe Applications**

    * Many DesignSafe Applications require that * You **specify the total number cores/node** 
    * The application will then compute the total number of cores automatically.

## Best Practices

* **Avoid hard-coding total core count.**

  * Instead, specify **cores per node** in your application inputs or job logic.
  * Let your script compute the total number of cores based on the number of nodes.
* This helps avoid errors if you later change the number of nodes but forget to update the total core count.

## Architectural Limits: CPU Cores, Shared Memory, and Process Counts per Node

Even though a compute node may offer many CPU cores (e.g. 56 or even 128 on Stampede3 SKX nodes), **all of those cores share the same pool of memory**. This shared-memory architecture means that if your job is memory-intensive, assigning one process per core can lead to **memory contention, degraded performance, or even job failure** due to insufficient RAM per process.

In such cases, it’s often more effective to **use fewer processes per node** to ensure that each has access to the memory it needs. For example, on a node with 192 GB RAM:

* Running **56 processes** gives \~3.4 GB RAM per process
* Running **24 processes** gives **8 GB RAM per process**
* Running **12 processes** gives **16 GB RAM per process**

This trade-off becomes especially important when:

* Running **MPI jobs** with large per-process memory usage
* Using **OpenSeesSP**, where each process loads significant data
* Executing **custom solvers** that don’t scale well with tightly packed cores

⚠️ You are always **limited by the number of physical cores per node**, but you are not required to use all of them. **Using fewer cores per node can give each process more memory headroom**, improving performance and reliability.

* **Example: Memory Per Process on a 192 GB Node**

    | **Processes per Node** | **Memory per Process** | **% of Cores Used** | **Cores Wasted** |
    | ---------------------- | ---------------------- | ------------------- | ---------------- |
    | 56                     | \~3.4 GB               | 100%                | 0                |
    | 32                     | 6 GB                   | 57%                 | 24               |
    | 24                     | 8 GB                   | 43%                 | 32               |
    | 12                     | 16 GB                  | 21%                 | 44               |

Understanding the balance between **CPU utilization and available memory** helps you design better HPC jobs—ones that not only run faster, but also more reliably. You don’t always want to max out the core count—**you want to match your process count to the memory your solver needs**.



