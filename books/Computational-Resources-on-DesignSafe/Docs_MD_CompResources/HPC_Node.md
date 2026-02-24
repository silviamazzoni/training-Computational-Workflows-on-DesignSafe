# Nodes

A **node** on TACC systems refers to a physical or virtual computing unit within the high-performance computing (HPC) cluster that is used to run computational jobs. 
- Each node typically consists of several CPU cores, memory (RAM), and access to storage and network interfaces. 
- Depending on the type of job and configuration, you can request multiple nodes to run parallel tasks.

In simple terms, a node is like an individual computer within the larger supercomputer. When you run jobs on TACC clusters (e.g., Stampede3), you are requesting access to nodes to perform computations.

## Each compute node on TACC systems typically includes:

| **Component**         | **Description**                                                                                  |
|-----------------------|--------------------------------------------------------------------------------------------------|
| **CPU (Cores)**       | Each node has multiple **cores** (e.g., Skylake nodes on Stampede2 have 48 cores per node).     |
| **Memory (RAM)**      | Memory available to the node. Typical compute nodes have 96 GB -- 192 GB of memory.              |
| **Network Interface** | High-speed network connection (e.g., Intel Omni-Path or InfiniBand) for inter-node communication.|
| **Local Disk**        | Temporary disk space local to the node for storing files during job execution.                  |

When you run jobs that require multiple nodes, the nodes communicate through a high-speed interconnect. These networks provide low-latency, high-bandwidth communication between nodes, making them ideal for distributed memory applications (e.g., MPI-based programs).

## Types of Nodes on HPC Systems

HPC systems such as TACC have different types of nodes, each optimized for specific workloads.

| **Node Type**            | **Description**                                                                                           |
|--------------------------|-----------------------------------------------------------------------------------------------------------|
| **Login Nodes**          | For submitting jobs, editing code, compiling programs, and interacting with the system.                   |
| **Compute Nodes**        | Where your computational jobs are *actually executed*. These nodes handle heavy parallel tasks.           |
| **GPU Nodes**            | Specialized nodes equipped with **GPUs** for tasks like AI, deep learning, and molecular dynamics.        |
| **Development Nodes**    | For testing and debugging. These nodes allow for short jobs with lower resource limits.                   |
| **Large-Memory Nodes**   | For memory-intensive applications (e.g., genome analysis, large simulations).                             |

## GPU vs CPU Nodes & Processors
The choice on which to use depends on the type of workload and the computational characteristics of the problem.

* **GPU Nodes (Graphics Processing Units)**
    - GPUs are designed to perform many calculations in parallel, making them ideal for data-parallel tasks. 
    - Each GPU typically has thousands of cores compared to CPU cores, but the GPU cores are simpler and optimized for parallelism.
    - Stampede3 hosts two types of GPU nodes, Intel's Ponte Vecchio and NVIDIA's H100 nodes, accessible through the pvc and h100 queues respectively.

* **CPU Nodes (Central Processing Units)**
    - CPUs have fewer cores (typically 4 to 64 cores per node) but are optimized for sequential tasks and general-purpose computing. 
    - CPU cores are more powerful individually compared to GPU cores and are suitable for tasks that don't parallelize well or require complex logic.

* **Quick Comparison**
    - CPUs have fewer, more powerful cores suited for general-purpose tasks.
    - GPUs have thousands of simpler cores optimized for parallel computing (e.g., simulations, AI). 
    - Some workloads benefit from both GPUs and CPUs working together in a **heterogeneous computing environment**. 
    - For example: Data Preprocessing (CPU) + Training (GPU): Use CPU nodes for preprocessing large datasets and feeding the data to GPU nodes for deep learning model training.


