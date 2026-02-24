# Stampede3 Nodes

The execution system on TACC used in this training module is **Stampede3**. 
- **Login Nodes**
    - The Stampede3 login nodes are Intel Xeon Platinum 8468 "Sapphire Rapids" (SPR) nodes, each with 96 cores on two sockets (48 cores/socket) with 250 GB of DDR.
    - These nodes are used for job testing and submittal, not for computation.
    - You can access these nodes via direct ssh login
- **Ice Lake Large Memory Nodes  NVDIMM**
    - **NVDIMM** in Ice Lake Large Mem nodes offers massive memory capacity (4 TB) but slower than DRAM.
- **Ice Lake Compute Nodes  ICX**
    - Stampede3 hosts 224 "Ice Lake" (**ICX**) compute nodes.
- **Sapphire Rapids Compute Nodes   SPR**
    - **SPR** nodes (Sapphire Rapids) offer 3.5x memory bandwidth per core, excellent for memory-bound apps.
    - Each SPR node provides a performance increase of 2 - 3x over the SKX nodes due to increased core count and greatly increased memory bandwidth. 
    - The available memory bandwidth per core increases by a factor of 3.5x. Applications that were starved for memory bandwidth should exhibit improved performance close to 3x.
- **Ponte Vecchio Compute Nodes   PVC**
    - **PVC** nodes include Intel GPUs--great for ML or GPU-accelerated workloads.
    - Each PVC GPU has 128 GB of HBM2e and 128 Xe cores providing a peak performance of 4x 52 FP64 TFLOPS per node for scientific workflows and 4x 832 BF16 TFLOPS for ML workflows.
- **Skylake Compute Nodes   SKX**
    - **SKX** nodes are older but still widely used--less powerful but more numerous.

## Stampede3 Node-Comparison Table

| Specification          | **Ice Lake (Large Mem)** | **Ice Lake (Compute)**  | **Sapphire Rapids (SPR)**  | **Ponte Vecchio (PVC)**  | **Skylake (SKX)** |
|------------------------|--------------------------|-------------------------|----------------------------|--------------------------|-------------------|
| **NODE**               | **NVDIMM**               | **ICX**                 | **SPR**                    | **PVC**                  | **SKX**           |
|------------------------|--------------------------|-------------------------|----------------------------|--------------------------|-------------------|
| **Special Notes**      | Large memory nodes       | Standard compute nodes  | High bandwidth & core count| GPU-accelerated nodes    | Legacy nodes. Less powerful by more numerous      |
| **Node Count**         | 3                        | 224                     | 560                        | 20                       | 1,060             |
| **CPU Model**          | Xeon Platinum 8380       | Xeon Platinum 8380      | Xeon MAX 9480              | Xeon Platinum 8480       | Xeon Platinum 8160 |
| **Cores/Node**         | 80 (2x40)                | 80 (2x40)               | 112 (2x56)                 | 96 (2x48)                | 48 (2x24)         |
| **Threads/Core**       | 1                        | 1                       | 1                          | 1                        | 1                 |
| **Threads/Node**       | 80                       | 80                      | 112                        | 96                       | 48                |
| **Clock Rate**         | 2.3 GHz (up to 3.4 GHz)  | 2.3 GHz (up to 3.4 GHz) | 1.9 GHz                    | 2.0 GHz                  | 2.1 GHz (1.4--3.7) |
| **RAM**                | 4 TB NVDIMM              | 256 GB DDR4             | 128 GB HBM2e               | 512 GB DDR5              | 192 GB DDR4       |
| **Cache per Socket**   | 110 MB (L2 + L3)         | 110 MB (L2 + L3)        | 168.5 MB (L2 + L3)         | 168.5 MB (L2 + L3)       | 57 MB (L2 + L3)   |
| **L1 Cache/Core**      | 48 KB                    | 48 KB                   | 48 KB                      | 48 KB                    | 32 KB             |
| **L2 Cache/Core**      | 1.25 MB                  | 1.25 MB                 | 1 MB                       | 1 MB                     | 1 MB              |
| **L3 Cache/Socket**    | 60 MB                    | 60 MB                   | 112.5 MB                   | 112.5 MB                 | 33 MB             |
| **Local Storage**      | 280 GB /tmp              | 200 GB /tmp             | 150 GB /tmp                | 150 GB /tmp              | 90 GB /tmp        |
| **GPU**                | --                       | --                      | --                         | 4x Intel Max 1550 GPUs   | --                |
| **GPU Memory**         | --                       | --                      | --                         | 128 GB HBM2e per GPU     | --                |


You can learn more about Stampede3 on the TACC documentation: [Stampede3 User Guide](https://docs.tacc.utexas.edu/hpc/stampede3/)
