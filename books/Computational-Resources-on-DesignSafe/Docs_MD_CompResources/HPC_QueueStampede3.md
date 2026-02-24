# Stampede3 Queues
On Stampede3, you specify a queue by specifying the node type to be used and, where possible, a special case of the node, such a large-memory, or development.

- **nvdimm** 
    - Ice Lake Large Memory Nodes  *NVDIMM*
- **icx**
    - Ice Lake Compute Nodes *ICX*
- **spr**
    - Sapphire Rapids Compute Nodes   *SPR*
- **pvc**
    - Ponte Vecchio Compute Nodes   *PVC*
- **skx**
    - Skylake Compute Nodes   *SKX*
- **skx-dev**
    - Skylake Compute Nodes -- Developer Queue  *SKX*
    - Development queue used for testing.
    - Maximum time limit of 2 hours
    - Wait times for development queue are very low.

### *skx-dev* Queue (Development / Testing Queue)

The **`skx-dev`** queue is a special development queue intended for **short testing and debugging runs**, not production workloads. It enforces strict limits to ensure fair access: you may run **only one job at a time**, and you may have **at most two jobs total in the queue** (one running and one waiting). If you submit additional jobs beyond this limit, they do not immediately enter the scheduler’s queue. Instead, they remain in a *blocked* state — effectively sitting in a “queue outside the queue” — and will only be admitted once space becomes available.

This queue is ideal for validating scripts, testing resource requests, debugging MPI or launcher behavior, and confirming job configuration before scaling up to larger production queues.



## Production Queues at TACC -- Limits on Stampede3
Below are the current (2025) Queue limits. These limits are subject to change without notice.[more](https://docs.tacc.utexas.edu/hpc/stampede3/#table8)

| **Queue Name** | Node Type | Max Nodes per Job (assoc'd cores) | Max Duration | Max Jobs in Queue | Charge Rate (per node-hour) |
|------------|-----------|------------------------------------|---------------|--------------------|------------------------------|
| **nvdimm**     | ICX       | 1 node (80 cores)                  | 48 hrs        | 3                  | 4 SUs                        |
| **icx**        | ICX       | 32 nodes (2560 cores)              | 48 hrs        | 12                 | 1.5 SUs                      |
| **spr**        | SPR       | 32 nodes (3584 cores)              | 48 hrs        | 24                 | 2 SUs                        |
| **pvc**        | PVC       | 4 nodes (384 cores)                | 48 hrs        | 2                  | 3 SUs                        |
| **skx**        | SKX       | 256 nodes (12288 cores)            | 48 hrs        | 40                 | 1 SU                         |
| **skx-dev**    | SKX       | 16 nodes (768 cores)               | 2 hrs         | 1                  | 1 SU                         |

## Production Queue Status
You can view the current status of each queue by accessing the [TACC portal](https://tacc.utexas.edu/portal/system-status/Stampede3). You may need to log in.


