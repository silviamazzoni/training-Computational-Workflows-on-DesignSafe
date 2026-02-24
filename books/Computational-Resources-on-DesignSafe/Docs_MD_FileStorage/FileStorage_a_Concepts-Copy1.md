# File Storage

***Understanding Storage on DesignSafe***

In high-performance computing (HPC), **every job either starts, ends, or both starts *and* ends with data**. Whether you’re running a small script or a large-scale simulation, your workflow involves reading input files and writing output results.

Understanding **where that data lives** — and how quickly it can be accessed or saved — is critical to optimizing both your **job performance** and your **research productivity**. Choosing the right storage location for each phase of your workflow helps avoid unnecessary slowdowns, data loss, or needless file transfers.

---

## Why File Storage Matters in HPC

When running jobs on HPC systems like Stampede3, **data input/output (I/O)** — reading and writing files — is often the **slowest part** of the workflow. Even with powerful CPUs and GPUs, your job can be bottlenecked if it is waiting on file access.

Optimizing **where** and **when** your data is accessed can significantly improve both **compute performance** and **researcher efficiency**. Selecting the correct storage system — whether it’s Corral, a compute system directory, or node-local scratch — ensures your simulations and analyses run smoothly.

---

## Storage Systems Overview

DesignSafe provides several storage areas, each serving a distinct purpose:

| Storage Type      | Description                                                                |
| ----------------- | -------------------------------------------------------------------------- |
| **MyData**        | Personal storage; your private "home" space.                               |
| **MyProjects**    | Project-specific collaborative storage shared among team members.          |
| **Work**          | High-performance project workspace for HPC jobs (fast, but not backed up). |
| **CommunityData** | Public datasets and shared examples (read-only).                           |
| **Published**     | Published datasets (NHERI, NEES), curated and citable (read-only).         |

> **Note:** *CommunityData* and *Published* are read-only and cannot be used for saving working files.

Additional **system-level directories** (e.g., *Home* and *Scratch* on Stampede3) exist and are covered in the **Compute Systems** section.


---

## DesignSafe Storage Path Examples

* **JupyterHub**
    
    Mounted paths, accessible directly in the notebook file browser. In JupyterHub, **all storage** systems have the same base path, making it very practical.
    
    | Type            | Example Path                            |
    | --------------- | --------------------------------------- |
    | MyData          | */home/jupyter/MyData/*                 |
    | Work            | */home/jupyter/Work/stampede3/*         |
    | Community       | */home/jupyter/CommunityData/*          |
    | MyProjects      | */home/jupyter/MyProjects/PRJ-...*      |
    | NHERI Published | */home/jupyter/NHERI-Published/PRJ-...* |
    | NEES Published  | */home/jupyter/NEES/*                   |


  
* **Stampede3**
    
    Traditional HPC with **absolute UNIX paths**. These are the paths you’ll use when:
    
    * SSH’ing into Stampede3
    * Writing batch scripts or Tapis job submissions
    
    | Type    | Example Path                         |
    | ------- | ------------------------------------ |
    | Home    | */home1/yourgroupid/jdoe/*           |
    | Work    | */work2/yourgroupid/jdoe/stampede3/* |
    | Scratch | */scratch/yourgroupid/jdoe/*         |
    
    To confirm your actual paths on the system:
    
    ```bash
    cd $HOME && pwd       # → /home1/05072/silvia
    cd $WORK && pwd       # → /work2/05072/silvia/stampede3
    cd $SCRATCH && pwd    # → /scratch/05072/silvia
    ```