# HPC Launchers
***Using HPC Launchers (e.g., PyLauncher) Inside a Tapis Job***

A Tapis job submitted to an HPC system is, at its core, a **standard Slurm batch job**. Once the job starts running on the execution system, everything that happens inside the allocation behaves exactly as it would if you had submitted the job manually with `sbatch`. This means you can safely and effectively use **HPC launcher tools** inside a Tapis job.

One commonly used example on TACC systems is **PyLauncher**.

PyLauncher is a Python-based parametric job launcher developed at TACC. Its purpose is to efficiently run **many small, independent tasks** within a single Slurm allocation by distributing them across all available cores and nodes. This makes it ideal for:

* Parameter sweeps
* Ensemble analyses
* Monte Carlo simulations
* High-throughput workloads with many short-running tasks

Because Tapis has already requested and reserved the compute nodes for your job, PyLauncher simply **inherits the Slurm allocation**. It detects the available resources by reading standard Slurm environment variables (such as node count, cores per node, and task layout) and uses them automatically.

**NOTE** The DesignSafe Agnostic App supports PyLauncher jobs.

### How PyLauncher Fits into a Tapis Job

The execution flow typically looks like this:

1. **Tapis submits the job to Slurm**

   * Nodes and cores are allocated according to your app definition (`nodeCount`, `coresPerNode`, etc.).

2. **The job starts on the primary node (Node0)**

   * Your `tapisjob_app.sh` wrapper script is executed.

3. **Environment setup**

   * Required modules are loaded (e.g., Python, PyLauncher).
   * Input files and parameters are already staged by Tapis.

4. **PyLauncher is invoked**

   * PyLauncher detects the Slurm allocation automatically.
   * Tasks are distributed across all nodes and cores.

From PyLauncher’s perspective, there is no difference between a manually submitted Slurm job and a Tapis-launched job—it simply sees a valid Slurm environment.

### Practical Usage in a Tapis App

To use PyLauncher in a Tapis app, you typically:

* Load the required modules (e.g., Python and PyLauncher)
* Prepare a task list (often a file containing one command per line)
* Invoke PyLauncher from within your app script

For example, many users rely on PyLauncher’s **ClassicLauncher**, which reads a list of shell commands and executes them concurrently—one per core—recycling cores as tasks complete.

This approach allows you to:

* Fully utilize all cores in your allocation
* Avoid submitting thousands of tiny Slurm jobs
* Keep scheduling overhead low while scaling throughput

---

## Developing Your Own Tapis App to Support Launchers and Advanced Workflows

Using tools like PyLauncher inside Tapis jobs is often the point where users move from **consuming existing apps** to **developing their own**.

### Why Write Your Own Tapis App?

Predefined Tapis apps are excellent for common workflows, but custom apps give you full control over:

* Job layout (nodes, cores, MPI vs non-MPI)
* Environment setup (modules, virtualenvs, containers, ZIP runtimes)
* Task orchestration (single run, loops, launchers, hybrid workflows)
* File staging and post-processing logic

If your workflow involves launchers, ensembles, or conditional logic, a custom app is usually the right next step.

### Key Design Pattern: Tapis as the Allocator, Launcher as the Dispatcher

A powerful mental model is:

> **Tapis allocates resources. Your app decides how to use them.**

In this model:

* Tapis requests the Slurm allocation and handles staging, bookkeeping, and monitoring.
* Your app script (`tapisjob_app.sh`) becomes the **orchestration layer**.
* Launchers like PyLauncher handle **intra-allocation parallelism**.


### Typical Structure of a Launcher-Aware Tapis App

When designing your own app, you usually define:

**In the app definition (`app.json` / `profile.json`):**

* Node count and cores per node
* Required modules (Python, PyLauncher, MPI, OpenSees, etc.)
* User-facing parameters (number of tasks, parameter ranges, input files)

**In the wrapper script (`tapisjob_app.sh`):**

* Load modules and activate environments
* Generate task lists dynamically (from parameters or input files)
* Invoke PyLauncher (or another launcher)
* Optionally collect and organize outputs

This separation keeps the app flexible and reusable while allowing complex runtime behavior.

### When Launchers Make the Most Sense

Using a launcher inside a Tapis app is especially effective when:

* Each task is relatively small compared to the allocation
* Tasks are independent (no inter-task communication required)
* You want to amortize Slurm queue wait time across many runs
* You need predictable, repeatable scaling behavior

For tightly coupled MPI simulations, you may rely on Slurm’s native MPI launch instead. But for **high-throughput and ensemble-style workflows**, launcher-based apps are often the most efficient solution.

---

### Takeaway

Tapis does not restrict how you use your allocated resources—it simply provides a structured, automated way to obtain them. By combining **custom Tapis apps** with **HPC launchers like PyLauncher**, you can build scalable, high-throughput workflows that are both powerful and reproducible, without sacrificing the flexibility of traditional Slurm-based HPC usage.

If you’d like, the next natural step would be:

* a **worked example** of a launcher-enabled Tapis app, or
* a **comparison** between PyLauncher, GNU Parallel, and MPI-based approaches inside Tapis.
