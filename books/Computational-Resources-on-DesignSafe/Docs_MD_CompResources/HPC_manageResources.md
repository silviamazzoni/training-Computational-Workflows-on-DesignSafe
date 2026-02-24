# Managing Your Resources

Managing your resources at TACC is an essential part of working productively on the systems. Resources include your projects, allocations (measured in Service Units or SUs), and storage spaces. Understanding how these are tracked and billed will help you avoid interruptions to your research and make the most of your compute time.

---

## 1. The TACC User Dashboard

The [TACC Dashboard](https://tacc.utexas.edu/portal/dashboard) is your primary tool for resource management. From this portal you can:

* View your **active projects** and associated allocations.
* Find your **allocation code**, which you’ll need when submitting jobs.
* Monitor your **remaining SU balance**.
* Check **system status** updates for current TACC machines.

*Note: usage figures in the dashboard may lag slightly behind actual job activity, so always allow for some delay in reporting.*

---

## 2. Understanding Allocations

When you run jobs on TACC systems, you are charged against an allocation of **Service Units (SUs)** that is tied to one or more projects. When your allocation is exhausted, you’ll need to request additional SUs before continuing work. Allocations are usually awarded through proposals, tied to specific funded projects, but started allocations are available upone request.

* **What you get:** A defined number of SUs assigned to each project.
* **When they run out:** You must submit a renewal or supplement request to add more SUs.
* **Why it matters:** Running jobs without an active allocation will fail.

---

## 3. How SUs Are Charged

TACC’s accounting system is based on **node-hours**: one SU = one node used for one hour.

**Formula:**

$$
\text{SUs billed} = (\# \text{nodes}) \times (\text{job duration in hours}) \times (\text{queue charge rate})
$$

Key rules:

* **Queue charge rates** differ by node type (e.g., GPU vs. standard CPU) and are adjusted for supply/demand.
* **Slurm-based billing** measures to the nearest few seconds; if your job ends early and exits properly, you are only charged for what you use.
* **No node sharing:** Each Stampede3 node is dedicated to one user. You are billed for the whole node regardless of how many cores you use.
* **Minimum charge:** Each job incurs a minimum of 15 minutes.

*Be aware that different Stampede3 queues (normal, development, GPU, etc.) charge different SU rates. Always check the documentation before running jobs.*

---

## 4. Monitoring Your Balance

* **Check regularly:** Use the TACC Dashboard to see your remaining SUs.
* **Plan ahead:** If you expect heavy use, submit a request for additional SUs early to avoid interruptions.
* **Stay efficient:** Tailor job requests to your actual needs (e.g., fewer nodes, shorter runtimes) to conserve SUs.

---

## 5. Requesting More SUs

When your project’s allocation is low, you’ll need to request more. The process depends on how your allocation was awarded:

* **ACCESS allocations:** Renew or supplement through the ACCESS portal.
* **TACC-only projects:** Request additional SUs through TACC’s allocation system or via your project PI.


---
## Key points to remember:

* The **queue charge rate** depends on supply and demand for the type of node you use. Rates may change over time.
* The **Slurm scheduler** charges based on actual usage, measured to the nearest few seconds. You are not billed for unused requested time—if your job ends early and exits cleanly, charges stop.
* **No node sharing:** On Stampede3, each node is dedicated to a single user. You will be billed for the entire node’s wall-clock time, regardless of how many cores you use.
* **Minimum charge:** All jobs incur a minimum charge of 15 minutes, even if they run for less time.
