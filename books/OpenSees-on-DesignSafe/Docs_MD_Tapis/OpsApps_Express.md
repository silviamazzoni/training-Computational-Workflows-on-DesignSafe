# OpenSees-EXPRESS App
***OpenSees-express: Lightweight Containerized OpenSees Runner***

The **OpenSees-express** app is a minimal and portable Tapis App that runs OpenSees inside a Docker container. It is designed for simplicity and reproducibility, making it ideal for quick tests, teaching environments, or scripted workflows that don’t require complex HPC scheduling or MPI parallelization.

Unlike the *OpenSeesMP* and *OpenSeesSP* apps, which are tailored for TACC HPC systems, *OpenSees-express* is:

* **Self-contained** — built entirely within a Docker container
* **Platform-flexible** — can be run on local, cloud, or development systems
* **Simple to use** — requires minimal job configuration

This app demonstrates how to wrap OpenSees using the Tapis platform with only three components:

1. A **Dockerfile** defining the container environment
2. An **app.json** file describing the Tapis app interface (inputs, outputs, parameters)
3. A **wrapper script** (*tapisjob_app.sh*) that handles runtime execution

Together, these files allow the app to be registered and used with any Tapis system that supports container-based execution, providing a clean and repeatable environment for running OpenSees models.


## Summary: A Lightweight, Reproducible App

The *OpenSees-express* app is a great example of how minimal a Tapis App can be:

| Component         | Purpose                                              |
| ----------------- | ---------------------------------------------------- |
| *Dockerfile*      | Creates a portable container with OpenSees installed |
| *app.json*        | Declares how the app should run and what it needs    |
| *tapisjob_app.sh* | Executes OpenSees with the user-supplied input file  |

This app is especially useful for:

* Small test cases
* Teaching and demonstrations
* Automation pipelines where speed and simplicity are key




