# Run DS Agnostic App
***Notebook Demo: Submitting OpenSees HPC Jobs with the Agnostic App***

This notebook demonstrates how to submit **OpenSees analyses** on DesignSafe using the **`designsafe-agnostic-app`**, a flexible Tapis application that supports **OpenSees, OpenSeesPy, and MPI-enabled workflows**.

While OpenSees-specific apps exist on DesignSafe, this demo focuses on the **agnostic execution path** to help you understand *exactly* how your analysis is launched on HPC systems — without hiding details behind presets.

---

### Why This Demo Exists

This notebook represents a **typical structural engineering workflow** on DesignSafe:

* OpenSees (Tcl or OpenSeesPy)
* Optional MPI execution
* Script-driven analysis
* Structured output handling

The purpose is not to teach OpenSees modeling, but to show how an OpenSees analysis fits into the **general DesignSafe execution model**.

By using the agnostic app, the demo makes all assumptions explicit — from the executable, to MPI usage, to directory layout.

---

### What to Watch For

As you go through the notebook, pay close attention to:

* How the **input directory** defines the OpenSees run

* How the job command mirrors a local OpenSees invocation:

  ```
  [ibrun] OpenSeesMP <input.tcl>
  ```

  or

  ```
  python OpenSeesPy_script.py
  ```

* How MPI behavior is **explicitly enabled or disabled**

* How environment modules and Python packages are set up

* How outputs are organized for:

  * large simulations
  * post-processing
  * batch or parametric studies

You’ll notice that only a **small number of inputs** differ from a non-OpenSees job — the execution flow itself is identical.

---

### What This Demo Is (and Is Not)

This notebook is:

* ✔ A complete OpenSees job submission example
* ✔ A transparent view of how OpenSees runs on HPC systems
* ✔ A reusable template for advanced OpenSees workflows

It is **not**:

* ❌ A full OpenSees modeling tutorial
* ❌ An MPI theory lesson
* ❌ A benchmark or performance comparison

The focus is on **execution mechanics**, not structural modeling theory.

---

### Key Takeaway

> **OpenSees on DesignSafe follows the same execution model as any other HPC job.**
> Once you understand this notebook, you can scale from a single analysis to large automated studies with confidence.
