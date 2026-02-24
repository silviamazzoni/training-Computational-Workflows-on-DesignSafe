# Working with Paths

***Why Paths Matter When Running Applications***

A **path** is the address of a file or directory. It tells applications—such as OpenSees, OpenSeesPy, or any Tapis app—**where to find inputs and where to write outputs** across your DesignSafe storage spaces (*MyData*, *MyProjects*, shared work areas) and compute systems like **Stampede3**.

Because DesignSafe spans **interactive environments (JupyterHub)**, **HPC systems**, and **automated job services (Tapis)**, understanding how paths behave across these environments is essential for building **reliable, portable workflows**.

---

## DesignSafe Storage Path Examples

DesignSafe exposes the *same underlying storage systems* through different environments, but **the paths you use depend on where you are working**.

### JupyterHub Paths (Mounted Storage)

In **JupyterHub**, DesignSafe storage systems are **mounted directly into the notebook filesystem**. All major storage locations share a common base path, making interactive work straightforward.

| Storage Type    | Example Path                             |
| --------------- | ---------------------------------------- |
| MyData          | `/home/jupyter/MyData/`                  |
| Work            | `/home/jupyter/Work/stampede3/`          |
| Community       | `/home/jupyter/CommunityData/`           |
| MyProjects      | `/home/jupyter/MyProjects/PRJ-.../`      |
| NHERI Published | `/home/jupyter/NHERI-Published/PRJ-.../` |
| NEES Published  | `/home/jupyter/NEES/`                    |

**Key idea:**
JupyterHub prioritizes *convenience*. You can browse, open, and write files using familiar Linux-style paths directly from notebooks.

---

### Stampede3 Paths (HPC Filesystems)

On **Stampede3**, you are working in a traditional HPC environment with **absolute UNIX paths**. These are the paths you’ll use when:

* SSH’ing into Stampede3
* Writing SLURM batch scripts
* Submitting jobs through Tapis

| Storage Type | Example Path                             |
| ------------ | ---------------------------------------- |
| Home         | `/home1/yourgroupid/username/`           |
| Work         | `/work2/yourgroupid/username/stampede3/` |
| Scratch      | `/scratch/yourgroupid/username/`         |

You can confirm your actual paths on Stampede3 using environment variables:

```bash
cd $HOME && pwd       # → /home1/05072/silvia
cd $WORK && pwd       # → /work2/05072/silvia/stampede3
cd $SCRATCH && pwd    # → /scratch/05072/silvia
```

**Key idea:**
HPC systems expect **explicit, absolute paths**. Assumptions that work in Jupyter often fail in batch jobs.

---

## Path Formats by Environment

Although you may be accessing the *same files*, the **path format depends on the execution context**.

| Environment    | Path Format             | Example                                                    |
| -------------- | ----------------------- | ---------------------------------------------------------- |
| **JupyterHub** | Mounted Linux paths     | `/home/jupyter/MyData/myfile.tcl`                          |
| **Stampede3**  | Absolute UNIX paths     | `/scratch/01234/username/project/run01/input.tcl`          |
| **Tapis**      | System + path reference | `tapis://designsafe.storage.community/myproject/input.tcl` |

> **Note:**
> In Tapis APIs and job definitions, you typically provide **`systemId` + `path`**, not a literal `tapis://` URI. The URI form is a convenient shorthand for documentation and mental mapping.

---

## Why Paths Behave Differently on DesignSafe

Even though everything lives under the DesignSafe umbrella, **compute and storage systems are physically separate**, and mounts differ by environment:

* All major file systems (*MyData*, *Community*, *Projects*, *Work*) live on the **Data Depot backend**, even if not all are visible in the web UI.
* **Stampede3 `/scratch`** exists only on the HPC system and is **not directly exposed** through the Data Depot.
* **`Work` is the critical bridge**:

  * Mounted on **JupyterHub**
  * Mounted on **Stampede3**
  * Accessible through **Tapis**
* Files written to **Scratch during a job** are **not visible** in JupyterHub or the Data Depot unless you explicitly copy them to **Work** or **MyData**.
* During a running job, the portal may expose a temporary *execution directory*, but this view is **transient** and should not be relied on for long-term storage.
* **Tapis can access all of these systems**, but only if you provide **paths that are valid for the target execution system**.

---

## Common Errors & Quick Fixes

* **“File not found” in jobs**
  → Use **full paths** or anchor relative paths to a known base directory.

* **Works in Jupyter, fails on HPC**
  → The working directory differs. Use **absolute paths** or expand `~` and environment variables.

* **Scratch outputs “missing” in Jupyter**
  → Copy results from **Scratch → Work or MyData** before inspecting them.

* **Spaces in paths**
  → Avoid them when possible. Otherwise, quote carefully or use `pathlib.Path`.

---

## Why This Matters

Understanding mounts and path semantics helps you avoid:

* Silent job failures
* Confusing “missing output” situations
* Fragile workflows that only work in one environment

With a clear path strategy, you can:

* Place inputs where jobs can read them efficiently
* Retrieve outputs reliably
* Write **portable workflows** that run across **JupyterHub, Tapis, and Stampede3** without modification

---

:::{admonition} One-Paragraph Takeaway
Relative paths are **shortcuts from where you’re standing** (your current working directory); full paths are the **complete address**. Jupyter favors relative convenience, but **HPC and Tapis workflows are safer with full paths and environment variables**. Use `pathlib` to compose paths cleanly, rely on **`Work`** as your bridge between Jupyter and Stampede3, and copy any **Scratch** results you want to keep into **Work** or **MyData**.
:::
