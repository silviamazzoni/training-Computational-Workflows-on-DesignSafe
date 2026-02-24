# Queues

When you submit a job to a high-performance computing (HPC) system like **Stampede3** via DesignSafe, you’re not running on a personal machine—you’re requesting access to **shared compute resources** that are managed through a **scheduler**. This scheduler organizes jobs into **queues**, which determine:

* **When** your job runs (based on priority and availability)
* **Where** your job runs (which nodes or partition)
* **How long** your job is allowed to run
* **How many nodes/cores/memory** you can request

Understanding queues and the **hardware structure of nodes** is essential to writing efficient, scalable, and stable jobs.

Choosing you queue wisely helps you:

* Get scheduled **sooner** (shorter jobs tend to start faster)
* Use system resources **more efficiently**
* Avoid wasting compute time with overly large or long requests

A **queue** is a submission line for jobs with similar resource requirements. Stampede3 offers multiple queues tailored for different job sizes and durations.

## Production Queues at TACC -- Limits
Production Queues have limits. These limits depend on the execution system and type of node/queue.

Limits are typically set on:
- Max Nodes per Job (assoc'd cores) 
- Max Duration 
- Max Jobs in Queue 
- Charge Rate (per node-hour)

**Note:** Your job must finish within the time limit, or it will be killed automatically.

## Production Queue Status
You can view the current status of each queue by accessing the [TACC portal](https://tacc.utexas.edu/portal/system-status). You may need to log in.


## When launching a job:

1. Estimate your **per-process memory requirement**
2. Multiply by the number of processes per node to ensure it fits within the node’s memory
3. Decide how many nodes you’ll need based on total core count and parallel strategy (e.g. MPI vs threads)
4. Choose the **queue** that fits your runtime and resource needs

By understanding the hardware, memory behavior, and queue structure of the HPC system, you’ll be better equipped to write jobs that run efficiently, scale effectively, and return results reliably.

