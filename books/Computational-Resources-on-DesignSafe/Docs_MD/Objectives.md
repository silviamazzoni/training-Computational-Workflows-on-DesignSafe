## Document Objectives

This module is intended to help users **understand and navigate the computational environments available on DesignSafe**, with particular emphasis on how interfaces, execution systems, middleware, and file storage interact.

Rather than teaching how to use a single application, this document focuses on the **infrastructure concepts** that enable scalable, reproducible, and efficient research computing. These concepts apply broadly across disciplines, tools, and analysis pipelines.

### In this module, you will learn how to:

* Understand the **computational resources provided through TACC**, and how different execution environments support interactive, batch, and large-scale HPC workloads.
* Distinguish between **interface environments** and **execution environments**, and understand how actions taken in one propagate to the other.
* Use DesignSafe’s **service and middleware layer** to connect user interfaces to execution systems, and understand the role this layer plays in job execution and monitoring.
* Work productively across multiple **interfaces**—including the Web Portal, JupyterHub, terminals, and APIs—and recognize when each is most appropriate.
* Understand **file storage systems and data lifecycles**, including:

  * where input files originate,
  * how files are staged for execution,
  * how intermediate and temporary data should be managed, and
  * how results are persisted and archived.
* Design computational practices that support **scalability**, **reproducibility**, and **efficient data management**, without being tied to a single workflow or application.

---

### By the end of this module, you will be able to:

* Explain **where and how computations run** when launched from different DesignSafe interfaces.
* Choose appropriate **execution environments** based on analysis size, runtime, and resource requirements.
* Navigate DesignSafe’s **storage systems** confidently, applying best practices for staging inputs, managing scratch data, and preserving results.
* Use interactive environments to prototype analyses while understanding how those prototypes translate to large-scale execution.
* Read application-specific and workflow-focused documentation with a clear mental model of the environments they rely on.

---

### Module Perspective

This module is structured to support a **conceptual progression**, not a procedural recipe.

It begins by establishing how users interact with DesignSafe, then moves inward to explain where computation occurs and how data flows across systems. Throughout, the focus remains on *why the platform is structured the way it is*, and how that structure enables research to scale—from small, interactive experiments to large, production-level computational studies.

By grounding workflow decisions in a solid understanding of computational environments and file management, this document equips readers with the context needed to use DesignSafe effectively—today and as their research grows more complex.
