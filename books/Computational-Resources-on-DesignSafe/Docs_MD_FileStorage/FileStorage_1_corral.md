# On File System
***The Backbone of DesignSafe Storage***

For **long-term, collaborative, and cross-platform data management**, DesignSafe uses **Corral**, a dedicated storage system fully integrated with the DesignSafe interface. Corral is the **central file system at TACC** that underpins most persistent storage in DesignSafe, including:

* **MyData** – Your personal, private storage space.
* **MyProjects** – Collaborative project storage where team members can share files.
* **CommunityData** – Public datasets and shared examples.
* **Published** – Finalized datasets that are publicly accessible and assigned DOIs for citation.

Think of Corral as the **foundation**: these different areas are simply directories with different access rules built on top of the same file system.

## Advantages of Corral

* **Persistent and backed up** — unlike Scratch or node-local storage, Corral is safe for long-term use.
* **Versatile access** — available through the **DesignSafe web portal (Data Depot)**, **JupyterHub**, **OpenSees Interactive VM**, and programmatically via **Tapis**.
* **Supports collaboration** — private (MyData) and group-based sharing (MyProjects).
* **Publication-ready** — data can be promoted into curated **Published datasets** with DOIs for citation.
* **Cross-platform consistency** — the same storage structure is visible across different environments.

## Limitations of Corral

* **Lower I/O performance** — Corral is network-mounted, so it’s slower than system-local storage (*Work* or *Scratch*) for large-scale compute jobs.
* **Not ideal for active job execution** — running HPC jobs directly from Corral can cause delays or job failures.

## Best Practice

* Use Corral (MyData/MyProjects) for **preparing input files**, **archiving results**, **team collaboration**, and **publication**.
* For active HPC jobs, **stage files to Work** on Stampede3, then move results back to Corral afterwards.

This architecture enables **cross-platform access**, **data sharing**, and **publishing workflows**, making Corral the **preferred data hub** in the DesignSafe ecosystem.
