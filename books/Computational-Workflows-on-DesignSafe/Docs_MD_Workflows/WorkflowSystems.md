# Workflow Systems

DesignSafe’s cyberinfrastructure brings together the **computational power of TACC** with the **ease of cloud-based interfaces**, allowing researchers to move seamlessly between interactive exploration and large-scale, production-level computation. Whether you’re testing a small python script inside a Jupyter notebook or deploying thousands of simulations across Stampede3, DesignSafe’s ecosystem is built to scale with you — from one core to tens of thousands.

While ***execution strategies*** describe *how computation should be structured*, then ***workflow systems*** describe *how those strategies are implemented, automated, and managed across real computing resources*.

At its heart, DesignSafe is not just a collection of tools — it is a **workflow system** designed to support the full life cycle of computational research:

* developing models and scripts,
* running and monitoring simulations,
* managing input and output data, and
* sharing or reproducing results.

Each of these stages may occur in a **different computational environment**, accessed through **different interfaces**, but connected by a **common middleware layer** that handles execution, authentication, and data transfer. This structure makes DesignSafe powerful, but it also means that understanding *how jobs flow through the system* is key to working efficiently and avoiding common pitfalls.

When you launch a job, the workflow system **orchestrates** a sequence of actions: your code or application is packaged, transferred to a compute system, queued by a scheduler, executed across one or more nodes, and finally collected and stored for postprocessing. Each of these steps occurs in a different **conceptual layer** of the architecture — the **interface environment**, the **execution environment**, and the **API layer** that connects them.

Understanding these layers helps you:

* choose the right tool for your task (interactive vs. batch, exploratory vs. production),
* optimize job performance and resource allocation,
* build automated, portable workflows that scale from prototypes to production, and
* troubleshoot or customize advanced workflows with confidence.

