# Environment Comparison

DesignSafe exposes multiple execution environments that differ in *interaction model*, *resource allocation*, and *scaling behavior*.

InDesignSafe, some applications, such as OpenSees, are available on Virtual Machines (VM). We are using the OpenSees-Express VM here as an example for comparison purposes.

### Feature Comparison

| Feature                 | JupyterHub (Interactive Containers) | HPC Environment (TACC Systems)                 | Virtual Machine (VM)                  |
| ----------------------- | ----------------------------------- | ---------------------------------------------- | ------------------------------------ |
| **Workflow Type**       | Interactive                         | Batch (queued)                                 | Immediate execution                  |
| **Access Mode**         | Browser-based notebooks & terminals | Web Portal, SLURM, SSH, or Jupyter for HPC     | Application dependent              |
| **Execution Model**     | User-driven, real-time              | Scheduler-driven                               | Backend service                      |
| **Typical Scale**       | Small to medium                     | Medium to very large                           | Small                                |
| **Parallel Computing**  | Limited                             | Yes (MPI, multi-node)                          | No                                   |
| **Resource Allocation** | Fixed per container session         | Explicitly requested per job                   | Shared VM resources                  |
| **Scheduling / Queue**  | Immediate (capacity permitting)     | Queued via SLURM                               | No queue                             |
| **Isolation Model**     | Dedicated container CPU/RAM         | Dedicated job allocation                       | Shared VM                            |
| **Interactivity**       | Full (live terminals & notebooks)   | Non-interactive (batch) or limited interactive | None                                 |
| **Ease of Use**         | High                                | Medium                                         | Very high                            |
| **Best Suited For**     | Development, testing, visualization | Production runs, large studies                 | Quick serial runs, entry-level usage |

---

### A Note on Virtual Machines in DesignSafe

DesignSafe provides **Virtual Machines (VMs) that are scoped to specific applications**, not to individual users.

* A VM may *appear* dedicated when accessed through a single application interface
* In practice, **multiple applications may run on the same underlying VM**
* Resources on that VM (CPU, memory, I/O) are therefore **shared**

In this guide, we refer to the **OpenSees-Express VM** as a convenient shorthand for the execution environment used by the OpenSees-Express application.
However, this VM is **not exclusively reserved for OpenSees**, nor is it guaranteed to be isolated from other workloads.

This distinction explains why:

* Execution is immediate (no queue)
* Resource limits are modest
* Performance can vary depending on concurrent activity

---

### How to Interpret These Environments

Rather than thinking in terms of *machines*, it is more accurate to think in terms of **execution models**:

* **JupyterHub** → interactive, container-isolated workflows
* **HPC systems** → scheduled, resource-explicit batch workflows
* **Application VMs** → simplified, shared backend execution

Each serves a distinct role, and many projects naturally move between them as complexity and scale increase.
