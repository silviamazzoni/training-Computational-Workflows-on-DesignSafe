# Job Arrays vs Launcher
***Which is better? Which is faster? let's compare them!***

Short version: on Stampede3, **“sarray” = Slurm job arrays** (*sbatch --array*), and **Launcher/PyLauncher = TACC’s parametric job launcher**. Neither is globally “better”; each wins in different regimes.

Below is a quick opinionated comparison, then some rules of thumb.

---

## Mental picture

* **Slurm job array (“sarray”)**
  One Slurm submission, but **many independent jobs** underneath, each with an index (*SLURM_ARRAY_TASK_ID*). Stampede3 explicitly supports them. ([TACC Documentation][1])

* **Launcher / PyLauncher job**
  **One Slurm job allocation**, inside which TACC’s launcher (or PyLauncher) runs a *workpile* (command list), feeding tasks to allocated cores until the list is exhausted. ([Texas Advanced Computing Center][2])

Historically TACC discouraged arrays on some systems and pushed Launcher/PyLauncher instead, but on Stampede3 both arrays and PyLauncher are available. ([Scribd][3])

---

## Side-by-side comparison

:::{dropdown} **1. Queue behavior & time-to-solution**


**Job arrays**

* Each array element is its **own schedulable job** (shares an ArrayJobId, but has its own JobId). ([Slurm Documentation][4])
* Slurm can start some tasks early via backfill, others later; they don’t all need to run at once.
* Overhead: scheduler handles *N* jobs. If you have thousands of **short** tasks (say 10–60 s), scheduler/launch overhead and file-system churn become noticeable.

**Launcher / PyLauncher**

* You **wait in the queue once** for a chunk of nodes; once you get them, Launcher or PyLauncher keeps them busy with many tasks until the paramlist is done. ([Texas Advanced Computing Center][2])
* For tiny tasks (seconds), this usually gives **better overall time-to-solution** because you:

  * amortize scheduler overhead across many tasks;
  * avoid flooding Slurm with thousands of jobs;
  * can keep nodes saturated even as tasks finish at different times.
* For long tasks (tens of minutes+), the advantage shrinks; queue behavior dominates.

**Rule of thumb**

* **Tasks ≥ 10–15 min each** → arrays *or* Launcher both fine.
* **Tasks ≤ a few minutes, thousands of them** → **Launcher/PyLauncher is usually faster in practice**.

:::

:::{dropdown} **2. Scheduler & policy friendliness**

TACC is big on **job bundling** and minimizing scheduler load; their job-bundling paper explicitly calls out Launcher/PyLauncher and friends for this use case. ([ACM Digital Library][5])

* Arrays are more scheduler-intensive when you push to large *N* (Slurm has a *MaxArraySize* and sites may set limits). ([Slurm Documentation][4])
* A single Launcher/PyLauncher job with a big command list often makes **TACC staff happier** for high-throughput/ensemble work.

So: if you’re doing Tapis-style thousands of short OpenSees runs / param sweeps, Launcher/PyLauncher is more aligned with TACC’s “job bundling” philosophy.

:::

:::{dropdown} **3. Implementation complexity**

**Job arrays**

* Script is simple: one Slurm script, one executable; vary inputs using *$SLURM_ARRAY_TASK_ID*. ([RCC Users][6])
* Good when each job looks like: “run this one command with a slightly different input file”.

**Launcher / PyLauncher**

* Requires **two pieces**:

  * the Slurm job script (requesting N nodes, etc.);
  * a **command list / paramlist** or a small Python snippet for PyLauncher. ([Texas Advanced Computing Center][2])
* Slightly more moving parts, but:

  * one line per task can be arbitrarily complex (different executables, options, working dirs);
  * PyLauncher has modes for threaded, MPI, GPU tasks, etc. ([TACC Documentation][7])

If your workload is already “one line per run” (e.g., your OpenSees param list), it maps *very* naturally to Launcher/PyLauncher.

:::

:::{dropdown} **4. Fault tolerance & restart**

**Job arrays**

* Each array element is an independent job:

  * if element 172 fails, you can just re-submit or rerun *--array=172* or *172-200*. ([RCC Users][6])
* Great when inputs are noisy and you expect some failures.

**Launcher / PyLauncher**

* Node failure generally kills the **entire** Slurm job, though the launcher may have completed many tasks already.
* PyLauncher has **restart/replay** support via restart files, but you have to set that up. ([TACC Documentation][7])

So: for messy workflows with lots of expected per-task failures, arrays can be simpler to reason about; for clean parameter sweeps, launcher is fine.

:::

:::{dropdown} **5. Resource usage & packing**

**Job arrays**

* Each element requests its **own resources** (nodes, tasks, memory).
* Slurm may pack array elements onto nodes efficiently, but from the user’s POV you don’t directly control “how many array tasks per node” beyond the resource requests.

**Launcher / PyLauncher**

* You explicitly pick **nodes x tasks**, and Launcher multiplexes your commands onto those cores.
* Easier to:

  * run several light jobs per core or per node (when they’re I/O-bound or low CPU);
  * tune concurrency (e.g., 8 tasks/node on SKX vs 28 on SPR, etc.) to match your app’s profile. ([TACC Documentation][1])

:::

---

## So which should *you* use on Stampede3?

### Use **Slurm job arrays (“sarray”)** when:

* Each task is **moderately heavy** (≥ 10–15 min);
* Every task looks essentially the same: *ibrun ./my_mpi_app ...* or *python script.py param*;
* You want:

  * native Slurm features (dependencies, array-task-limited runs with *--array=1-1000%32*, etc.);
  * easy per-task monitoring, accounting, and failure handling.

### Use **Launcher / PyLauncher** when:

* You have **lots of small or medium tasks**, especially:

  * 10^2–10^5 runs;
  * runtimes from a few seconds to a few minutes;
* You want to **bundle** them into one Slurm job to:

  * reduce scheduler and filesystem stress;
  * improve aggregate throughput;
  * keep a node allocation saturated with work;
* You need flexibility:

  * heterogeneous commands (different apps/args per line);
  * multi-threaded or MPI jobs in the same workpile (PyLauncher). ([TACC Documentation][7])

---

## Direct answer to three questions

* **Which is “better”?**
  
  *Policy-wise* on Stampede3: for classic HTC/param sweeps, **TACC leans toward Launcher/PyLauncher** as the recommended tool; arrays are fine but easier to abuse at scale. ([ACM Digital Library][5])

* **Which is “faster”?**

  * For **short/high-count** tasks → Launcher/PyLauncher generally gives **better time-to-solution**.
  * For **long, heavy** tasks → performance difference is negligible; pick whichever scripting model is nicer for you.

* **Main differences/advantages in one sentence:**

  * **Job arrays**: many independent Slurm jobs, simple *$SLURM_ARRAY_TASK_ID* logic, great for medium/long embarrassingly parallel runs with clean per-job accounting.
  * **Launcher/PyLauncher**: one Slurm job acting as your own mini-scheduler, ideal for **bundling huge ensembles of small/medium jobs** while being friendly to the scheduler and file system.



[1]: https://docs.tacc.utexas.edu/hpc/stampede3/?utm_source=chatgpt.com "Stampede3 User Guide - TACC HPC Documentation"
[2]: https://tacc.utexas.edu/research/tacc-research/launcher/?utm_source=chatgpt.com "The Launcher - Texas Advanced Computing Center"
[3]: https://www.scribd.com/document/787452419/EijkhoutHPCtutorials?utm_source=chatgpt.com "Eijkhout HPCtutorials | PDF | Computer File"
[4]: https://slurm.schedmd.com/job_array.html?utm_source=chatgpt.com "Job Array Support - Slurm Workload Manager - SchedMD"
[5]: https://dl.acm.org/doi/fullHtml/10.1145/3437359.3465569?utm_source=chatgpt.com "Tools and Guidelines for Job Bundling on Modern ..."
[6]: https://users.rcc.uchicago.edu/~tszasz/rccdocs/running-jobs/array/index.html?utm_source=chatgpt.com "Job Arrays — Research Computing Center Manual"
[7]: https://docs.tacc.utexas.edu/software/pylauncher/?utm_source=chatgpt.com "PyLauncher at TACC"
