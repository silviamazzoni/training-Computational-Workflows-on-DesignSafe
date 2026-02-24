# Paths in Tapis Applications
***How Storage Is Referenced in Jobs***

Tapis provides a unified way to access storage systems, but **paths are never standalone**. Every path is interpreted **relative to a system**.

---

## System + Path (The Core Concept)

In Tapis, file locations are defined using:

* ***systemId*** → where the file lives
* ***path*** → where it is on that system

Conceptually:

```
(systemId, path)
```

Documentation often shows this as:

```
tapis://systemId/path/to/file
```

…but this is shorthand. APIs and job definitions always separate the two.

---

## Common DesignSafe Storage Systems

| Storage Location | Typical System ID              |
| ---------------- | ------------------------------ |
| MyData           | *designsafe.storage.default*   |
| Work             | *designsafe.work.stampede3*    |
| Community        | *designsafe.storage.community* |
| Scratch (HPC)    | *designsafe.compute.stampede3* |

---

## Example: Input File Reference

```json
{
  "sourceSystemId": "designsafe.storage.default",
  "sourcePath": "/myfolder/input/model.tcl"
}
```

This tells Tapis exactly **where** to fetch the file from.

---

## Output Locations Matter

If your app writes output to:

```bash
/scratch/05072/silvia/run01
```

Those files will **not automatically appear** in JupyterHub or the Data Depot.

Best practice:

* Write **final outputs** to *WORK* or *MyData*
* Or explicitly copy them at the end of your job

---

## Why Tapis Paths Feel Strict (and That’s Good)

Tapis enforces clarity:

* No ambiguous relative paths
* No implicit working directories
* No guessing which system you meant

This discipline is what allows:

* Web-submitted jobs
* Automated pipelines
* Reproducible workflows

---

## Summary: Tapis Path Rules of Thumb

* Always think **system first, path second**
* Scratch is **fast but temporary**
* Work is the **bridge**
* Final results belong in **Work or MyData**

---

# Designing Path-Safe, Reproducible Workflows

***From Interactive Exploration to Scalable Runs***

Paths are not just technical details—they encode **workflow intent**.

A good path strategy answers:

* Where do inputs live?
* Where do intermediate results go?
* Which outputs should persist?

---

## Recommended Directory Roles

| Location | Purpose                                       |
| -------- | --------------------------------------------- |
| MyData   | Inputs, scripts, notebooks, long-term storage |
| Work     | Active runs, shared staging, job outputs      |
| Scratch  | High-performance temporary computation        |

---

## Example Workflow Pattern

```
MyData/
 └── projectA/
     ├── inputs/
     ├── scripts/
     └── notebooks/

Work/
 └── projectA/
     ├── run01/
     ├── run02/
     └── results/

Scratch/
 └── projectA/
     └── run01_tmp/
```

---

## Portability Principle

Your **code should not change** when moving between:

* Jupyter exploration
* Single-node tests
* Large-scale HPC runs

Only paths and environment variables should differ.

---

## Common Anti-Patterns to Avoid

* Hard-coding */home/jupyter/...* in batch jobs
* Writing final results only to Scratch
* Relying on implicit working directories
* Mixing inputs and outputs in the same folder

---

## The Big Picture

Path-safe workflows enable:

* Debugging in Jupyter
* Scaling on HPC
* Automation through Tapis
* Sharing with collaborators

They are foundational—not optional—for serious computational research on DesignSafe.
