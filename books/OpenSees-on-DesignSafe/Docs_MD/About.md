# About This Document

This document is a comprehensive guide to running OpenSees within the DesignSafe ecosystem — from interactive experimentation to large-scale high-performance computing (HPC) simulations on TACC systems.

While OpenSees itself is a modeling framework, deploying it effectively on DesignSafe requires understanding a larger computational architecture that includes:

* Web-based interfaces
* JupyterHub interactive environments
* Tapis middleware services
* SLURM-based HPC execution on TACC systems
* Distributed storage systems (MyData, MyProjects, Work, Scratch)
* Application wrappers and job schemas

This document explains how these layers connect — and how OpenSees workflows move through them.

Although the examples focus on:

* **OpenSees (Tcl)**
* **OpenSeesPy**
* **OpenSeesMP**
* **OpenSeesSP**

the architectural principles apply to other scientific and engineering workflows on DesignSafe.

This is not simply a click-through tutorial. It is a structured reference that:

* Explains how execution works under the hood
* Connects OpenSees command structure to HPC environments
* Clarifies how Tapis maps to SLURM
* Documents app schemas and wrapper logic
* Demonstrates scalable automation strategies

Hands-on training notebooks and step-by-step workflows are included throughout the document, but they are embedded within a broader systems-level explanation.

The goal is not just to show how to run a job — but to help you understand what happens when you do.