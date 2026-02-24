# About This Document

DesignSafe provides access to powerful computational resources through TACC, but using those resources effectively requires understanding **how computation, data, and interfaces fit together**. This document is designed to provide that foundation.

Rather than focusing on a single application, this book introduces the **computational workflow architecture of DesignSafe** — explaining how analyses move from user-facing interfaces, through middleware services, onto compute systems, and back again as results. The emphasis is on **how the platform works as a system**, and how researchers can design workflows that scale from interactive exploration to large, automated studies.

## How This Book Is Organized

This book is organized into several complementary layers:

* **Computational workflow concepts**
  Introduces common workflow patterns (interactive, batch, automated) and the architectural components that support them.

* **Compute environments**
  Describes the execution environments available on DesignSafe — including JupyterHub, HPC systems, and virtual machines — and explains when and why each is appropriate.

* **SLURM and batch execution**
  Provides a scheduler-level view of how jobs are submitted, scheduled, and executed on TACC systems, forming the basis for scalable computation.

* **Tapis and Tapis Apps**
  Introduces the middleware layer that connects user interfaces to compute resources, including job submission, monitoring, automation, and application abstraction.

* **Python utilities and training notebooks**
  Supplies reusable tools and hands-on notebooks that demonstrate how these concepts are applied in practice and how workflows can be automated programmatically.

* **File storage and data movement**
  Explains how data is staged, accessed, moved, and persisted across systems, which is essential for building reliable workflows.


These sections are designed to be **modular**. While the book can be read sequentially, many chapters also serve as **reference material** that users may return to as their workflows evolve.

---

## Relationship to Application-Specific Documents

This document establishes a **general framework for computational research workflows on DesignSafe**. Application-focused documents (such as those for OpenSees, OpenFOAM, or ADCIRC) build on this foundation by applying the same concepts to specific tools.

Those documents are intended as **worked examples**, not prerequisites. Understanding the workflow architecture presented here will make it easier to adapt to new applications and computational methods over time.

---

## Python Utilities Library Used in This Document

Throughout the notebooks and examples in this book, a **custom Python function library** is used to support common workflow tasks such as job submission, monitoring, file management, and data inspection. This library is stored in **DesignSafe Community Data** and is actively maintained.

* While the library can be copied directly, this is **not recommended**, as it is updated regularly.
* Each notebook includes a **small setup snippet near the top** showing how to reference or copy a stable version of the library into your own workspace. This approach balances reproducibility with ongoing improvements.