# Storage Options

DesignSafe gives you three main storage systems, each designed for a different phase of the research lifecycle.

* **Corral** is the **long-term home** for your data. It lives on a **networked storage system at TACC**, with automatic **backups** and strong support for **collaboration and publication**. Corral is accessible from almost everywhere in DesignSafe — the Data Depot, JupyterHub, VMs, and via Tapis Apps. Think of Corral as your research “filing cabinet”: it’s where data is safely stored, shared with collaborators, and archived for future reuse.

* **Work** is mounted directly on compute systems for **active projects**, so it offers **high performance** but without backups. It’s ideal for **staging inputs** before you run jobs and **holding outputs** afterward.

* **Node-local storage** is attached to the compute node your job runs on. It’s **ephemeral** and disappears when the job ends, but it’s extremely fast and useful for **scratch space** during computation.

Here’s a compact table that shows at a glance how Corral, Work, and Node-local differ in persistence, performance, and access. 



| Storage Type   | Persistence                    | Performance        | Access From                             | Best Use Case                         |
| -------------- | ------------------------------ | ------------------ | --------------------------------------- | ------------------------------------- |
| **Corral**     | Long-term, backed up           | Moderate (network) | Data Depot, JupyterHub, VMs, Tapis      | Archiving, collaboration, publication |
| **Work**       | Long-term (not backed up)      | High (on system)   | Compute systems, Data Depot, JupyterHub | Staging input/output files for jobs   |
| **Node-local** | Temporary (deleted at job end) | Very High (local)  | Only during active compute job          | Fast scratch I/O during runtime       |

You can immediately see why Corral is for **long-term use**, while Work and node-local are for **jobs**. 

This table makes the tradeoffs clear:

* **Corral** = safe, shared, persistent → but slower.
* **Work** = faster, system-mounted, but not backed up.
* **Node-local** = fastest, but ephemeral.

*Prepare in Corral → Run in Work/Node-local → Archive back to Corral!!*
