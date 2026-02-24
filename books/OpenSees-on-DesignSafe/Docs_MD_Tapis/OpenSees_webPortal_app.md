# The OpenSees Web Portal App

The **DesignSafe Web Portal app** provides a **graphical user interface (GUI)** for running OpenSees and OpenSeesPy jobs without writing code or job scripts.

It is especially valuable for:

* **Exploring and understanding app inputs**
* **Validating execution settings**
* **Testing small or first-time runs**
* **Learning how an app is structured before automating it**

This means you can:

* Focus on your structural or geotechnical model — not on cluster commands.
* Submit jobs through a simple browser interface (or later, programmatically through Tapis or Python).
* Get consistent, optimized performance on TACC hardware without fighting with compilers, environment modules, or manual SLURM scripts.

  
For many users, the Web Portal is the **first and most intuitive entry point** into OpenSees on DesignSafe.

---

## What the Web Portal Does Well

The Web Portal excels as an **interactive configuration and validation tool**:

* Every input field is clearly labeled and documented.
* Required vs optional inputs are explicit.
* Default values are visible and editable.
* Resource requests are constrained to valid ranges.
* Execution mode choices are clearly presented.

This makes the portal an excellent way to:

* Understand what an app expects
* Catch input errors early
* Confirm that a workflow runs correctly before scaling
* Learn by inspection rather than trial-and-error

In practice, many users rely on the Web Portal to **prototype a job** before moving to scripted or programmatic submission.

---

## Why the Web Portal Does Not Scale

While the Web Portal is extremely useful, it is **not designed for scalable or automated workflows**.

Limitations include:

* Jobs must be submitted **manually, one at a time**
* Repetitive parameter studies require repeated clicking
* No native support for:

  * parametric sweeps
  * batch generation
  * programmatic control
  * integration with external pipelines
* Difficult to reproduce complex workflows exactly
* Not suitable for version-controlled workflows

As studies grow in size and complexity, these constraints become limiting.

---

## How the Web Portal Fits into the Bigger Picture

The Web Portal should be viewed as:

> **A configuration and learning interface — not a workflow engine**

A very effective pattern is:

1. **Use the Web Portal** to:

   * explore inputs
   * read documentation
   * validate a small run
2. **Transition to Tapis or Python**:

   * once inputs are understood
   * when scaling or automation is required

This pattern works equally well for:

* legacy OpenSees apps
* OpenSeesPy
* the agnostic app

---

## Relationship to the Agnostic App

The Web Portal remains extremely valuable **even with the agnostic app**:

* The agnostic app exposes more flexibility and options
* The Web Portal helps users **understand those options visually**
* Once validated, the same inputs can be:

  * reused
  * scripted
  * parameterized
  * automated

In other words:

> The Web Portal is often the **best place to start**,
> but **not the place to stay** for large or repeatable workflows.

---

## Recommended Usage Pattern

* **Web Portal**

  * Learn
  * Explore
  * Validate
  * Prototype

* **Agnostic App via Tapis / Python**

  * Scale
  * Automate
  * Reproduce
  * Extend

This division of roles keeps the workflow both **approachable** and **powerful**.

