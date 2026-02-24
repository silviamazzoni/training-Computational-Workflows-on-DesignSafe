# OpenSees Apps on DesignSafe

Running OpenSees on an HPC system like Stampede3 isn’t as simple as typing a single command. In a traditional HPC workflow, users would need to:

* Write a **SLURM batch script**, specifying resources, queues, and walltime
* Load the correct **environment modules** for OpenSees, MPI, and Python
* **Stage input files** to scratch space for performance
* Launch the analysis using the correct **MPI or serial execution model**
* **Collect outputs** back into long-term storage
* Debug failures related to environment setup rather than modeling

These steps are essential for efficient HPC use, but they require deep familiarity with Linux, SLURM, and system-specific conventions.

To lower this barrier, DesignSafe provides **Tapis applications** that automate job setup, submission, execution, and file management for OpenSees workflows. These apps encapsulate the complexity of SLURM, environment configuration, and data staging, allowing users to focus on their analysis rather than the mechanics of the HPC system.

Over time, two complementary approaches to OpenSees execution on DesignSafe have emerged:

* **Application-specific (legacy) OpenSees apps**, which provide highly streamlined interfaces for common OpenSees execution modes, and
* A **generalized (agnostic) app**, which exposes a more flexible execution model capable of supporting OpenSees, OpenSeesPy, and non-OpenSees workflows alike.

Both approaches rely on the same underlying HPC infrastructure and submission mechanisms, but they differ in **scope, flexibility, and intended use**. The legacy apps prioritize simplicity and ease of use, making them ideal for well-defined, traditional OpenSees workflows. The agnostic app prioritizes scalability and extensibility, enabling more advanced, automated, and multi-tool workflows at the cost of requiring a bit more user understanding.

The following sections describe each approach in detail and explain how to choose the one that best fits your workflow.


---

## How to Think About App Choice Today

* Use **legacy OpenSees apps** if:

  * you want the simplest possible interface
  * you are running a classic OpenSees workflow
  * you prefer minimal configuration

* Use the **agnostic app** if:

  * you want flexibility
  * you plan to scale workflows
  * you are combining tools
  * you want access to newer features
  * you are automating or scripting submissions

The agnostic app is now the **recommended foundation** for new workflows.
