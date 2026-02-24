# Paths in Python on DesignSafe
***Writing Portable, Environment-Aware Code***

When working in Python—especially across **JupyterHub**, **HPC jobs**, and **Tapis-launched workflows**—hard-coded strings quickly become brittle. Python provides tools that let you **compose, resolve, and validate paths safely**, regardless of where your code runs.

---

## Why *pathlib* Matters

Python’s *pathlib* module treats paths as **objects**, not strings. This makes code:

* More readable
* Less error-prone
* Easier to adapt across environments

```python
from pathlib import Path

base = Path("/home/jupyter/MyData")
input_file = base / "models" / "frame01.tcl"

print(input_file)
# /home/jupyter/MyData/models/frame01.tcl
```

Advantages over string paths:

* Automatically inserts */*
* Supports *.exists()*, *.is_dir()*, *.resolve()*
* Works naturally with relative paths

---

## Relative vs Absolute Paths in Practice

In notebooks, **relative paths often work** because the current working directory (CWD) is stable:

```python
Path("inputs/model.tcl")
```

But in batch jobs or Tapis apps, the CWD may be:

* A temporary execution directory
* A staging folder created at runtime

**Best practice:**
Resolve paths early and explicitly.

```python
model_path = Path("/work2/05072/silvia/stampede3/projectA/input/model.tcl")
```

---

## Using Environment Variables

DesignSafe and TACC define useful environment variables:

```python
import os
from pathlib import Path

work = Path(os.environ["WORK"])
scratch = Path(os.environ["SCRATCH"])

run_dir = scratch / "opensees" / "run01"
```

This allows your code to adapt automatically when run:

* In JupyterHub
* On Stampede3
* Inside a Tapis job

---

## Validating Paths Early

Fail fast when files are missing:

```python
if not input_file.exists():
    raise FileNotFoundError(f"Missing input: {input_file}")
```

This is especially important for **long HPC jobs**, where silent failures waste queue time.

---

## Summary: Python Path Rules of Thumb

* Use ***pathlib.Path***, not raw strings
* Resolve paths **before** launching analyses
* Prefer **absolute paths** for batch jobs
* Use **environment variables** for portability

The notebooks in the Training Sections will build on these principles directly.


