# OpenSees Legacy Apps on DesignSafe
***Application-Specific Legacy OpenSees Tapis Apps***

DesignSafe has long provided the following **OpenSees-specific Tapis apps**, each targeting a particular execution mode:

* **OpenSeesEXPRESS** – sequential (single-core) OpenSees
* **OpenSeesMP** – MPI-based parallel OpenSees
* **OpenSeesSP** – distributed-processing OpenSees
* **OpenSeesPy** – Python-based OpenSees workflows (NEW!)

These apps are:

* **Simple to understand**
* **Purpose-built**
* **Well suited for early adoption**
* **Highly approachable for new HPC users**

Each app wraps a familiar OpenSees execution pattern and hides the complexity of SLURM, file staging, and environment setup.

That simplicity is intentional — and valuable.

---

## Where These Apps Run

* **OpenSeesMP**, **OpenSeesSP**, and **OpenSeesPy** run on **Stampede3**, submitted through the SLURM scheduler.
* **OpenSeesEXPRESS** runs on a **virtual machine**, bypassing the HPC queue and typically starting immediately.

This distinction reflects historical usage patterns and resource needs rather than architectural preference.

---

## Why These Apps Exist — and Their Limits

From a *user* perspective, these apps work very well.

From a *developer* perspective, however, they all do essentially the same thing:

* Stage input files
* Configure an execution environment
* Generate a SLURM job
* Launch an executable
* Collect outputs

The differences between them are largely:

* **which executable is run**
* **how MPI is invoked**
* **how many resources are requested**

Maintaining many nearly identical apps:

* duplicates logic
* increases maintenance cost
* makes it harder to add new features consistently
* slows innovation

As DesignSafe workflows matured, this model became **unsustainable**.

---

## The OpenSeesPy App: A Transitional Step

The **OpenSeesPy app** deserves special mention.

It was developed as a **bridge**:

* to support Python-based workflows
* to align with existing OpenSees app conventions
* to ease early adoption of OpenSeesPy on HPC

Architecturally, however:

> **OpenSeesPy is a strict subset of what the agnostic app can do.**

It exists for consistency and continuity — not because it represents a fundamentally different execution model.

