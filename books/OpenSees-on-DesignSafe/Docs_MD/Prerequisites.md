# Prerequisites

This document focuses on **how to run OpenSees within the DesignSafe ecosystem**, not on how to build structural models from first principles.

You do not need to be an OpenSees expert to benefit from this guide — but you should have some familiarity with how OpenSees works conceptually.

---

## Expected Background

You will benefit most from this document if you:

* Have run at least one **OpenSees (Tcl)** or **OpenSeesPy** script before
* Understand what an OpenSees input script looks like
* Are familiar with basic structural modeling concepts (nodes, elements, materials, sections, loads, analysis commands)
* Have a general sense of what your model is intended to do

You do *not* need:

* Deep knowledge of OpenSees internals
* Advanced parallel computing experience
* Prior experience with SLURM
* Prior experience with Tapis APIs

Those infrastructure and execution concepts are explained here.

---

## What This Document Does Not Cover

This document is not:

* A full OpenSees user manual
* A modeling theory guide
* A tutorial on structural analysis fundamentals
* A comprehensive MPI programming reference

If you are completely new to OpenSees modeling, you may want to first explore:

* Introductory OpenSees examples
* Basic OpenSeesPy tutorials
* Simple single-degree-of-freedom or 2D frame examples

Then return to this document to learn how to deploy those models on DesignSafe.

---

## Technical Familiarity (Helpful but Not Required)

Some exposure to the following will be helpful:

* Basic command-line usage
* File and directory structures
* Python scripting (for OpenSeesPy workflows)

However, this guide introduces HPC execution, resource selection, job submission, and middleware concepts in a structured and gradual way.

---

## Mindset

More than specific technical skills, what you need is:

* A willingness to think in terms of workflows
* Curiosity about what happens “under the hood”
* An interest in scaling your simulations beyond your local machine

This document bridges modeling and infrastructure — helping you move from *running a script* to *designing a reproducible computational workflow*.
