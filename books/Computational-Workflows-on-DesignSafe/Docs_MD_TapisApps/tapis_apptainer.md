# What Is Apptainer?

**Apptainer is a container runtime designed specifically for HPC (High-Performance Computing).**
It provides the same core functionality as Docker—packaging your software and environment into a portable, reproducible container—but it is built to work **without root privileges**, which is essential in shared supercomputing environments.

It is:

* **Open-source**, governed by the Linux Foundation
* **The successor to Singularity** (the project was renamed starting in 2021)
* **The standard on HPC systems**, where Docker is typically prohibited

Most people in HPC still casually say “Singularity,” but the modern software stack and project name is **Apptainer**.

---

## Why HPC Uses Apptainer Instead of Docker

Supercomputers do **not** allow root access or privileged daemons. Docker requires:

* A root-owned daemon (`dockerd`)
* Privileged operations (namespaces, cgroups, mounts)

This is unsafe on multi-user HPC clusters.

Apptainer, however:

* Runs containers **as the user**, with the same permissions the user already has
* Does **not** require a daemon
* Plays nicely with job schedulers like **Slurm**, **PBS**, **LSF**, etc.
* Integrates with shared filesystems (Lustre, GPFS, NFS)

This makes Apptainer the “official container runtime” for academic HPC.

---

## How an Apptainer Container Works

An Apptainer container is typically a single **immutable `.sif` file**:

```
mycontainer.sif
```

This file contains:

* A full Linux filesystem (like an OS image)
* Installed software/packages
* Executables, libraries, Python environments, etc.

You run it like this:

```bash
apptainer run mycontainer.sif
```

or:

```bash
apptainer exec mycontainer.sif python script.py
```

It **feels** like Docker, but the security model and execution model are very different.

---

## Apptainer vs Docker (quick comparison)

| Feature                   | Docker               | Apptainer                     |
| ------------------------- | -------------------- | ----------------------------- |
| Requires root?            | **Yes**              | **No**                        |
| Designed for HPC?         | ❌ No                 | **✔ Yes**                     |
| Runs under Slurm?         | Not allowed          | Standard                      |
| File is a single `.sif`?  | No                   | **Yes**                       |
| Can import Docker images? | —                    | **✔ Yes**, converts to `.sif` |
| User isolation            | Strong               | User-level, HPC-safe          |
| Supports GPUs, MPI?       | Yes (but not on HPC) | **Yes**, HPC-native           |

**Big point:**
Apptainer can **pull and convert** Docker images:

```bash
apptainer build my.sif docker://pytorch/pytorch
```

This makes it the bridge between Docker ecosystems and HPC ecosystems.

---

## How This Relates to Tapis Apps on DesignSafe

When your Tapis app specifies:

```json
"runtime": "SINGULARITY"
```

…it is essentially running through **Apptainer** on Stampede3 or Frontera.

The app’s:

```json
"containerImage": "/work/.../myapp.sif"
```

is the Apptainer/Singularity image file.

Inside the job, Tapis runs something like:

```bash
apptainer run myapp.sif args...
```

(Older docs say “singularity run,” but on TACC systems the backend is now Apptainer.)

---

## When You Should Use Apptainer in Your Apps

Use Apptainer (**runtime = SINGULARITY**) when:

* You want a **self-contained, portable environment**
* You want to ensure the software stack is the same everywhere
* Your app needs custom Python/conda, exotic libraries, or OS-level dependencies
* You want to run the same container on Jetstream2, TACC, and another cluster

Do **not** use it if:

* You want extremely fast iteration and don’t want to rebuild images
* You’re happy with TACC modules → in this case, use **ZIP runtime** instead

---

## Simple definition you can include in your documentation

> **Apptainer (formerly Singularity)** is the container engine used on HPC systems because it runs securely without root privileges. It packages your application and its full software environment into a single portable `.sif` image and executes entirely within user space, making it the standard container runtime for Tapis apps on DesignSafe’s HPC resources.
