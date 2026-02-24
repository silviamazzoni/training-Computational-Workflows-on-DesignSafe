# About This Document

DesignSafe provides access to powerful computational resources through its close integration with the Texas Advanced Computing Center (TACC). While these resources enable advanced, large-scale analyses, using them effectively requires a clear understanding of **how interfaces, execution systems, middleware, and data environments fit together**.

This document is designed to provide that foundation.

Rather than focusing on a specific scientific application or a particular workflow pattern, this book explains the **computational environments that underpin research computing on DesignSafe**. It describes where users interact with the platform, where computations actually run, how services connect those layers, and how data moves between them. The emphasis is on understanding DesignSafe as an **integrated system**, rather than as a collection of individual tools.

A central theme throughout this document is **location and context**:

* Where commands are issued
* Where jobs execute
* Where files reside at different stages
* How data persists (or does not) across environments

Understanding these distinctions is essential for building efficient, scalable, and reproducible computational work.

### How This Book Is Organized

This book is organized around the **core components of the DesignSafe computational ecosystem**, rather than around applications or workflows.

* **Interface environments**
  Describes where users interact with DesignSafe, including the Web Portal, JupyterHub, terminals, and programmatic APIs. These chapters focus on *how users access resources* and *what capabilities each interface provides*.

* **Execution environments**
  Explains where computations run, including HPC systems, batch queues, compute nodes, and virtualized resources. Emphasis is placed on understanding execution context, resource allocation, and system boundaries.

* **Middleware and service layers**
  Introduces the services that connect interfaces to execution systems, particularly Tapis. This section focuses on *what the middleware does* and *how it shapes execution*, without diving into workflow design details covered elsewhere.

* **File storage and data management**
  Covers how data is staged, accessed, moved, cached, persisted, and archived across environments. Topics include shared filesystems, scratch space, input/output staging, intermediate files, and long-term storage strategies.

These sections are intentionally **modular**. While the book can be read from start to finish, many chapters are designed to serve as **reference material** that users can return to as their computational needs evolve.

### Relationship to Other Documents

This document provides the **environmental foundation** for computational research on DesignSafe.

Companion documents focus on:

* Workflow design and orchestration
* SLURM behavior and job scheduling
* Tapis job submission, automation, and scaling
* Application-specific usage (e.g., OpenSees, OpenFOAM, ADCIRC)

Those materials build on the concepts introduced here. By understanding the environments described in this book, readers will be better prepared to apply workflow patterns, automation strategies, and application-specific guidance across a wide range of use cases.
