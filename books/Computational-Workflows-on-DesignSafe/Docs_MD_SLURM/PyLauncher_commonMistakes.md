# Common Mistakes
***Common Mistakes in Using Pylauncher and How to Avoid Them**

**❌ Writing all runs to the same output directory**

**Problem:**
Multiple tasks overwrite files or fail unpredictably.

**Fix:**
Ensure **every command writes to a unique output folder**:

```text
--outDir outCase41
--outDir outCase42
```

---

**❌ Expecting output in tapisjob.out**

**Problem:**
You don’t see OpenSees or Python output where you expect it.

**Why:**
PyLauncher captures stdout/stderr **per task**, not globally.

**Fix:**
Look inside the PyLauncher-created subdirectory in your **inputDirectory**.
Each task has its own log files.

---

**❌ Viewing PyLauncher logs in the Data Depot**

**Problem:**
Files appear unreadable or empty.

**Why:**
PyLauncher log files often have **no file extension**.

**Fix:**
Use **JupyterHub** to inspect PyLauncher output files.

---

**❌ Forgetting to disable MPI**

**Problem:**
Jobs hang, crash, or behave inconsistently.

**Fix:**
Set:

```
UseMPI = false
```

when submitting the job.

---

**❌ Using PyLauncher for tightly coupled workflows**

**Problem:**
Jobs fail or produce incorrect results.

**Why:**
PyLauncher is for **independent serial tasks**, not coupled simulations.

**Fix:**
Use MPI directly (outside PyLauncher) for coupled models.
