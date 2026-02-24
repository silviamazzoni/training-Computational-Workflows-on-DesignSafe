# HPC Resources
***Understanding the TACC HPC Resources***

## Core Concepts You’ll See Throughout This Module

These terms will be referenced **again and again** — feel free to click into any linked term for a deeper explanation, or simply return to this list later as needed:

* **Node**: A full physical machine allocated to your job. Independent computing units. A single node typically contains multiple CPU cores and a set amount of memory. You request nodes using the `nodeCount` attribute in Tapis.
* **Core**: A single CPU within a node; jobs can run in parallel across multiple cores.
* **Cores per Node**: The number of CPU cores available on each node. For example, on Stampede3, each compute node has 48 cores. This is set using the `processorsPerNode` attribute.
* **Memory per Node**: The amount of RAM available on each node. Memory capacity can vary between queues and systems. Tapis allows you to request this via `memoryPerNode`.
* **Queue (Partition)**: helps determine *when* your job runs, based on runtime and resource requirements. It's a waiting line for jobs, organized by system, job type, and size. You select a queue using the `batchQueue` attribute. 
    

* **Allocation**: Your granted share of computing resources, like CPU hours or access to specific systems. All jobs consume Service Units (SUs) from a TACC allocation. These allocations define how much compute time you can use on a given system.
* **SLURM**: The job scheduler (workload manager) that dispatches your jobs to available nodes.
* **SLURM Job File**: is a script that defines your job’s inputs, resources, and runtime behavior. Job parameters include cores, memory, wall time, and commands.

Each of these plays a role in how your job is scheduled, executed, and monitored.

Depending on system load and job size, your **queue wait time** may be shorter or longer than the job’s actual runtime.Efficient HPC usage requires balancing your resource request: requesting too much can increase wait time, while too little may cause job failure or underperformance.



## HPC Hardware Architecture at TACC

TACC systems consist of hundreds or thousands of **compute nodes**, each with:

* Dozens of CPU cores (e.g., 48 on Stampede3),
* Shared memory (RAM),
* High-speed network interconnects for parallel communication.

* Here's a conceptual diagram showing how **nodes**, **cores**, **queues**, and **allocations** are organized within TACC systems:

    ```
    +-----------------------------------------------------------+
    |                  TACC High-Performance System             |
    |                                                           |
    |  +-------------------+   +-------------------+            |
    |  |    Queue: skx     |   |  Queue: skx-dev   |            |
    |  |-------------------|   |-------------------|            |
    |  | +---------------+ |   | +---------------+ |            |
    |  | |  Node 1       | |   | |  Node A       | |            |
    |  | | Core 0        | |   | | Core 0        | |            |
    |  | | Core 1        | |   | | Core 1        | |            |
    |  | | ...           | |   | | ...           | |            |
    |  | | Core 47       | |   | | Core 47       | |            |
    |  | +---------------+ |   | +---------------+ |            |
    |  | +---------------+ |   | +---------------+ |            |
    |  | |  Node N       | |   | |  Node M       | |            |
    |  | +---------------+ |   | +---------------+ |            |
    |  +-------------------+   +-------------------+            |
    |                                                           |
    |  Allocations track total usage across queues and systems  |
    +-----------------------------------------------------------+
    ```

* **Notes:**
    
    * Each **queue** (e.g., `skx`, `development`, `normal`) manages a pool of compute nodes.
    * Each **node** contains a fixed number of **CPU cores** (e.g., 48 on Stampede3).
    * Your **TACC allocation** defines how many total **Service Units (SUs)** you can spend across the system.
    * Tapis jobs specify how many nodes and cores to request from a given queue.

