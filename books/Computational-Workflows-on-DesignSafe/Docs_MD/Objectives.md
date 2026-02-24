# Document Objectives

In this training module, you’ll learn **how to design, execute, and manage computational research workflows within DesignSafe**, using its full range of computational environments — including the **Web Portal**, **JupyterHub**, **Tapis**, and **direct HPC command-line access**.

Rather than focusing on a single application, this module emphasizes the **core concepts and infrastructure** that underpin scalable, reproducible, and efficient research workflows on DesignSafe. These principles apply broadly across scientific and engineering domains and can be adapted to many tools, models, and analysis pipelines.

Specifically, this module will help you learn how to:

* Understand the **hardware architecture available through TACC**, and how different types of analyses map to interactive, batch, and large-scale HPC systems.
* Use the **software and service layer** that supports computation at scale — including **Tapis**, the **Tapis API**, and **task-specific Tapis Apps** — to automate and manage research workflows.
* Work effectively across multiple **computational interfaces**, from browser-based tools and Jupyter notebooks to terminals and batch scripts, and understand when each approach is most appropriate.
* Structure workflows so they can grow from **exploratory, interactive analyses** to **large, automated production runs** without rewriting everything from scratch.
* Navigate **DesignSafe data storage systems**, including best practices for data staging, file movement, intermediate results, and long-term archival.

---

## By the end of this module, you’ll be able to:

* **Use the DesignSafe Web Portal** to launch computational jobs using preconfigured applications, without manually writing batch scripts.
* **Work within JupyterHub** to prototype analyses, generate inputs dynamically, and submit computational jobs programmatically.
* **Run applications from a terminal or notebook**, understanding how scripts, environment variables, and runtime context interact.
* **Submit batch jobs to TACC HPC systems via SLURM**, specifying computational resources such as nodes, cores, memory, and wall time.
* **Automate parameter studies and ensembles**, using scripting and workflow logic to scale analyses efficiently.
* **Leverage Tapis programmatically** to submit, monitor, manage, and retrieve results from multiple jobs as part of a larger research workflow.

---

## Module Roadmap: From Interactive to Scalable Workflows

This module is organized as a **progressive journey through DesignSafe’s computational ecosystem**, following the natural evolution of a research workflow.

It begins with **interactive and exploratory environments**, such as the DesignSafe Web Portal and JupyterHub, where users can inspect data, prototype analyses, and develop scripts. From there, it introduces **batch-oriented and high-performance computing concepts**, showing how the same analyses can be executed more efficiently on TACC systems using SLURM and Tapis-managed jobs.

As the module progresses, the focus shifts from *how to run a single job* to *how to manage many jobs*: automating parameter studies, organizing data movement, monitoring execution, and retrieving results programmatically. Throughout, emphasis is placed on understanding **why** a particular environment or workflow choice is appropriate, not just **how** to use it.

Application-specific examples (such as OpenSees) are used to ground these ideas in real workflows, while keeping the core principles broadly applicable. By the end of the module, learners should be able to move confidently from small, interactive experiments to **robust, scalable research workflows** on DesignSafe.




