# Virtual Machines (VMs)

DesignSafe also provides access to dedicated **Virtual Machines (VMs)** for lightweight and quick-turnaround OpenSees workflows. These systems are distinct from the JupyterHub environment and are optimized for **non-parallel simulations**.

## OpenSees-Express VM

### Execution Model

* The **OpenSees-Express VM** is a **submit-only environment**.

  * This VM has 1 node, 48 cores and 49GB of RAM (wma-exec-01.tacc.utexas.edu)
  * You cannot SSH into the machine or use it interactively.
  * Jobs are sent to the VM via **Tapis**, typically using:

    * The **Web Portal** -- OpenSees Tcl only
    * A Tapis job from a Jupyter notebook (via Tapipy)

### Shared Environment
* Jobs are executed on a **single VM node** shared across multiple users.

  * Unlike containers on JupyterHub, the VM does **not enforce per-user isolation**.
  * Users share **CPU, memory, and disk I/O**, which can cause performance variation under heavy load.


## Retirement of Interactive VM

DesignSafe previously offered a legacy **OpenSees Interactive VM**, which allowed users to connect to a shared environment for live execution. This environment is being retired in favor of the more scalable and modern **JupyterHub** system, which offers similar capabilities with better resource management and isolation.

## When to Use OpenSees-Express

* When you need to run **short, sequential Tcl jobs** quickly, with no queue delay.
* When jobs don’t require MPI or multi-threading.
* When you want to submit jobs through a point-and-click interface with minimal setup.
