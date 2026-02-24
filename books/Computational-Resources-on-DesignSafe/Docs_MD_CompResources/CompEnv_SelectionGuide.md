# Selection Guide
***A Practical Guide to Selecting a Compute Environment**

Choosing the right compute environment depends on two primary questions:

1. **How do you want to interact with your computation?**
2. **How large and resource-intensive is your problem?**

---

**Step 1 — Interaction Style**

Ask yourself:

* Do I need to *interact* with the computation while it runs?
* Am I developing or debugging code?
* Do I want notebooks, plotting, or scripting in real time?

If yes → start with an **interactive environment**.

If no → a **batch workflow** is likely appropriate.

---

**Step 2 — Scale and Resources**

Next, consider resource requirements:

* Fits within modest CPU and memory limits
  → Interactive environments are often sufficient
* Requires long runtimes, many cores, or MPI
  → Batch HPC execution is required

---

## A Simple Decision Guide

* I’m exploring, learning, or prototyping
  → **JupyterHub**

* I want to run a small serial script with minimal setup, (e.g. OpenSees)
  → **OpenSees-Express VM**

* I need large-scale, long-running, or parallel execution
  → **HPC batch jobs on TACC systems**

---

## Choosing the Optimal Compute Environment

| Environment                | Access Method                | Resources & Scaling                     | Best For                                               |
| -------------------------- | ---------------------------- | --------------------------------------- | ------------------------------------------------------ |
| **JupyterHub**             | Browser (notebooks/terminal) | Up to 8 cores / 20 GB RAM per container | Prototyping, OpenSeesPy, quick test loops, automation            |
| **OpenSees-Express VM**    | Web Portal (form-based)      | Shared lightweight VM                   | Tcl scripts, small serial jobs, easiest point of entry |
| **HPC Environment** | SSH + SLURM (Tapis)            | Full system access, massive scale                  | Parallel OpenSees jobs, large simulations, production  |

---

### A Typical Compute Path

Many users naturally follow this progression:

1. Develop and test interactively
2. Validate on small problems
3. Scale up using batch jobs
4. Automate or repeat studies at scale

This transition is expected — and supported — within the DesignSafe ecosystem.


---

### Why This Matters

Understanding *where* your computation runs — and *how* it is executed — helps you:

* Avoid unnecessary queues
* Use resources efficiently
* Scale smoothly from prototypes to production
* Reduce friction as projects grow
