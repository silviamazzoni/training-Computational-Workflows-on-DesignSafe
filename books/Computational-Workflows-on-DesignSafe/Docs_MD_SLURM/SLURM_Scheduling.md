# Job Scheduling
***TACC Scheduling & Policy Considerations***

TACC uses a **fair-share priority system** to schedule jobs across all its users. This system aims to maximize both fairness and overall system efficiency, ensuring that compute resources are available to as many researchers as possible.

## How the fair-share scheduler works

* **Recent usage matters:**
  If you’ve recently run many large jobs, your future jobs might be temporarily assigned lower priority, giving other users an opportunity to access the system. Over time, your share resets, so this is dynamic and balances out.

* **Job size and duration influence scheduling:**

  * **Shorter jobs and jobs requesting fewer nodes or cores often start sooner**, because they can easily fit into smaller available time slots on the cluster.
  * Large jobs might wait longer for enough resources to free up simultaneously.

* **Special queues:**
  TACC systems offer special queues with different policies. For example:

  * `development` queues are intended for small, short test jobs and generally have very short maximum wall-times (often 30 minutes to a few hours).
  * `gpu` queues have policies specific to GPU resource allocation.
  * Other queues may exist for large-scale or priority projects.

## Recommendations for designing your workloads

* **Is it better to submit many small jobs or a few large jobs?**

    It depends on your specific workload and goals:
    
    | When to prefer **many small jobs**            | When to prefer **fewer large jobs**                    |
    | --------------------------------------------- | ------------------------------------------------------ |
    | - Parameter sweeps / independent simulations  | - Large tightly coupled parallel jobs (MPI)            |
    | - Monte Carlo or uncertainty quantification   | - When memory or compute needs exceed small job limits |
    | - Tasks that don't need to talk to each other |                                                        |
    
* **Advantages of many small jobs:**
    * Often start sooner, fit into open slots on the scheduler.
    * Lower risk of long queue times if cluster is busy.
    * Easier to rerun if one fails.
    
* **Advantages of fewer large jobs:**
    * Necessary for problems that require all processors working together (large finite element models, CFD, etc.).
    * Potentially more efficient due to reduced I/O overhead between jobs.


## Best practices before submitting your jobs

Following these practices helps your jobs run faster, use fewer resources, and keep the system fair for everyone:

:::{dropdown} **Test small first**

Always test your scripts on small examples or in the `development` queue.
This avoids wasting allocation time on avoidable errors and ensures your input files are valid before scaling up.

:::

:::{dropdown} **Right-size your requests**

Request only the wall time and number of cores or nodes you truly need:

* **Overestimating** makes your job wait longer in the queue.
* **Underestimating** means your job might be killed before it finishes.

:::

:::{dropdown} **Use job arrays or automation for parameter studies**

If you’re running many small, independent simulations (like a parameter sweep or Monte Carlo study), look into **SLURM job arrays** or Python/Tapis automation to handle them efficiently.
This often gives you **better throughput** than one giant job.

:::

:::{dropdown} **Understand your queue’s policy**

Each TACC queue has different limits:

* Maximum wall times, node/core restrictions, and intended use (e.g. `development` is for short runs).
* For example, Stampede3’s normal queue allows up to 48 hours, while the development queue may cap you at 2 hours.

:::

:::{dropdown} **Plan for restarts or checkpoints**

Especially for long jobs. This way, if something fails or the system goes down, you don’t lose all your progress.

:::

:::{dropdown} **Be a good cluster citizen**

* Clean up large scratch files when your job completes.
* Monitor your fair-share usage so others get access too.
* Avoid tying up resources longer than necessary.

:::

:::{dropdown} **Keep your fair-share impact in mind**

* Many smaller jobs often start sooner and can fill open gaps on the scheduler.
* But for problems that require many processors working tightly together (like large MPI OpenSeesMP jobs), submitting fewer larger jobs is unavoidable and necessary.
:::


## Summary

* TACC’s fair-share system means your priority adjusts over time based on your usage and the needs of others.
* Smaller, shorter jobs generally get scheduled faster because they help fill in gaps in cluster availability.
* Always design your computational approach with flexibility in mind — break large studies into multiple jobs when possible, but use large jobs only when the problem’s architecture demands it.


