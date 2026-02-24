# Run DS Agnostic App
***Notebook Demo: Submitting General HPC Jobs with the Agnostic App***

This notebook demonstrate how to submit computational jobs on DesignSafe using the **`designsafe-agnostic-app`**, a **general-purpose Tapis application** for running arbitrary workloads on HPC systems.

The focus here is not on a specific scientific domain, but on **how jobs are constructed, submitted, and executed** on DesignSafe. If you understand these notebooks, you understand the **core execution model** behind most automated workflows on the platform.

This demo intentionally uses a **pure Python workflow** to emphasize that the agnostic app is **not tied to any particular software stack**.

A similar notebook for OpenSees jobs is shown in the OpenSees-On-DesignSafe Document.

---

### Why This Demo Exists

This notebook showcases a **general Python workflow** that:

* Does **not** rely on OpenSees or any domain-specific tools
* Runs exactly as it would on the command line
* Uses the same submission mechanics as more complex HPC jobs
* Demonstrates how DesignSafe handles:

  * execution context
  * environment setup
  * input/output staging
  * reproducibility

The goal is to show that if you can describe a job in terms of:

```
<executable> <script> <arguments>
```

then you can run it through the agnostic app.

---

### What to Watch For

As you work through the notebook, pay attention to these recurring patterns:

* The **input directory** defines the execution context
* The job command mirrors a standard command-line invocation
* MPI usage (or lack thereof) is **explicitly controlled**
* Software environments are **declared, not assumed**
* Outputs are organized to support:

  * large result sets
  * automation
  * downstream workflows

These patterns apply broadly across DesignSafe — regardless of the application or discipline.

---

### What This Demo Is (and Is Not)

This notebook is:

* ✔ A practical, end-to-end job submission example
* ✔ A reusable template for general workflows
* ✔ Representative of how most Tapis jobs are constructed

It is **not**:

* ❌ A machine-learning tutorial
* ❌ A performance optimization guide
* ❌ Domain-specific training material

The emphasis is on **workflow mechanics**, not scientific content.

---

### Key Takeaway

> **The agnostic app is a general execution driver.**
> If you can run a job from the command line, you can run it on DesignSafe using this pattern.
