# Python within Python
***Managing Python Scripts from a Notebook***

Let's look at executing a Python Script from a Jupyter Notebook: What your options are, how they differ, and when variables stick around.

Sometimes you want to run a full script from a notebook—maybe to reuse a workflow, pass command‑line args, or isolate heavy computations. 

There are several ways to do it, and they differ mainly in **process isolation** and **variable scope** (whether variables persist in the notebook after the run):


**Option 1 — *%run script.py [args]* (same kernel, variables persist)**

::::{dropdown} Runs the file **in the current IPython kernel**. 
Your script executes as if it were *__main__*, and when it finishes, the variables it defined are available in the notebook.

```python
# notebook cell
%run run_openseespy.py --nx 10 --ny 5

# If run_openseespy.py defines 'disp_top' and 'reactions'
disp_top[:5], reactions.get('base')
```

:::{dropdown} Inside run_openseespy.py
```
import argparse
import openseespy.opensees as ops

p = argparse.ArgumentParser()
p.add_argument('--nx', type=int, default=10)
p.add_argument('--ny', type=int, default=5)
args = p.parse_args()

ops.wipe()
ops.model('BasicBuilder', '-ndm', 2, '-ndf', 3)
# ... build, analyze ...
disp_top = [0.001, 0.002, 0.003]  # example
reactions = {'base': -123.4}
```
:::

* **Keeps variables?** Yes. Objects created in the script are available after it runs.

**When to use:** You want results (arrays, dicts, models) to **stick around** in the notebook for immediate plotting.

> Tip: If the script needs to **read** notebook variables (Access notebook vars inside the script?), use `-i`:

```python
nx, ny = 10, 5         # notebook variables
%run -i run_openseespy.py
```

* **Pass CLI args?** Yes: accessible via *sys.argv* in the script.
* **Good for:** Iterating on a script while keeping results and objects in memory.


::::

**Option 2 — *!python script.py [args]* (separate process, no shared variables)**

::::{dropdown} Runs the script in a **new OS process** (a real shell command).

Runs the script as a **true shell command** — perfect for CLI parity or isolating heavy runs.
To pull results back, **write them to files** (CSV/JSON/NPZ) and then read them in the notebook.

```bash
# notebook cell
!python run_openseespy.py --nx 10 --ny 5 --out results.json

# bring results back into the notebook
import json
with open('results.json') as f:
    res = json.load(f)
res['reactions']['base']
```

:::{dropdown} Inside `run_openseespy.py`:

```python
import argparse, json
import openseespy.opensees as ops

p = argparse.ArgumentParser()
p.add_argument('--nx', type=int, default=10)
p.add_argument('--ny', type=int, default=5)
p.add_argument('--out', default='results.json')
args = p.parse_args()

# ... OpenSeesPy setup/run ...
out = {
    'disp_top': [0.001, 0.002, 0.003],
    'reactions': {'base': -123.4}
}
with open(args.out, 'w') as f:
    json.dump(out, f)
```
:::

**When to use:** You want OS-level isolation, CLI behavior, or to mimic production/batch runs.
**Remember:** Variables **do not** persist to the notebook; use files for data exchange.

* **Keeps variables?** No. The script can only communicate back through **files**, **stdout/stderr**, or **return codes**.
* **Capture output?** Yes:

  ```bash
  lines = !python my_script.py
  print("\n".join(lines))
  ```
* **Good for:** True command‑line behavior, isolation, testing CLI tools, or when you want the script to run exactly as it would outside Jupyter.

::::


:::

**Option 3 — *import module* then call functions (modular approach)(function + returns)**

:::{dropdown} Turn your script into a **module** (e.g., put functions in *mylib.py*) and import it. 
Refactor your script into functions and call them directly. Cleanest for testing and re-use.
You stay in the notebook kernel and call functions explicitly.

```python
# notebook cell
import myopensees as mops
disp_top, reactions = mops.run_model(nx=10, ny=5)
```

**Inside `myopensees.py`:**

```python
import openseespy.opensees as ops

def run_model(nx=10, ny=5):
    ops.wipe()
    ops.model('BasicBuilder', '-ndm', 2, '-ndf', 3)
    # ... build, analyze ...
    return [0.001, 0.002, 0.003], {'base': -123.4}
```

* **Keeps variables?** Yes. You decide what to keep by assigning returned values.
* **Edit-and-rerun?** Use reload:

  ```python
  import importlib, mylib
  importlib.reload(mylib)
  ```
* **Good for:** Clean, testable code; calling individual functions; keeping state in the notebook.
* **When to use:** You want proper APIs, unit tests, and easy reloading.

:::

**Option 4 — *%run -m package.module [args]* (run as a module)**

:::{dropdown} Like *%run*, but uses Python’s *-m* module execution 
(resolves packages on *sys.path*):

```python
%run -m mypackage.tools.train --epochs 5
```

* **Keeps variables?** Yes (same as *%run*), results become available after execution.
* **Good for:** Running package entry points without hardcoding file paths.
:::

**Option 5 — *%load script.py* (bring code into a cell)**

:::{dropdown} Loads the script’s source **into the current cell**
So you can edit/execute it interactively.

```python
%load my_script.py
# (Code appears in the cell — edit and run. Variables will live in the notebook.)
```

* **Keeps variables?** Yes—because you execute the code *as cell code* in the notebook’s namespace.
* **Good for:** Learning, tinkering, line‑by‑line debugging, or gradually refactoring a script into cells.

:::

**Option 6 — *subprocess* (fine‑grained shell control)**

:::{dropdown} When you need more control than *!python* 
(timeouts, env vars, binary pipes):

```python
import subprocess, sys
result = subprocess.run(
    [sys.executable, "my_script.py", "a", "b"],
    capture_output=True, text=True, check=False
)
print(result.stdout)
```

* **Keeps variables?** No (separate process), but you can capture output, exit codes, and manage environments.
:::

---

## Variables & State: quick reference

* **%run**: runs in the **same kernel**; variables created in the script are available after.

  * **%run -i** also lets the script **read** variables that already exist in your notebook.

* **!python** / **subprocess**: runs in a **different process**; **no variables** are shared. Use files/stdout to pass data back.

* **import**: you control what persists by calling functions and capturing returns; module objects are accessible as *module.name*. Use *importlib.reload* when you edit the module.

* **%load**: pulls the script’s **source** into a cell; once you execute the cell, everything lives in the notebook namespace.

---

## MPI & batch notes (OpenSeesPy)

* If you need **parallel (MPI)**, launch the script with `mpiexec` from a terminal or batch system:

  ```bash
  mpiexec -n 4 python run_openseespy.py --nx 10 --ny 5
  ```
* Jupyter kernels are **single-process**; MPI across nodes generally won’t work in one kernel. Use HPC batch, Tapis, or SLURM.
* For **embarrassingly parallel** sweeps in a notebook, prefer `concurrent.futures` (single node) or submit multiple jobs via Tapis/SLURM arrays for multi-node.

---

## Which one should I use?

* **Need to pass CLI args →** *%run script.py args...* **or** *!python script.py args...* (both work; *%run* keeps variables, *!python* isolates).
* **Keep variables in notebook?** → *%run* (or *%run -i*) **or** import the script as a **module** and call functions.
* **True CLI isolation / production parity?** → *!python* **or** *subprocess* (write results to files).
* **Refactor for cleanliness & reuse?** → import as a module (functions + returns).
* ***Develop* the script interactively →** *%load* (then run/edit in cells) **or** convert to functions and *import*/*reload*.


---
## Notes for OpenSeesPy users

* Running an entire OpenSeesPy script with *%run* or *!python* is **non‑interactive**: the file executes top‑to‑bottom and the program exits when done (recommended for batch runs).
* If you want **interactive** development with plots and stepwise control, import OpenSeesPy in cells and run commands directly; keep heavy/batch runs as scripts.
* Parallel (MPI) runs usually **won’t** work inside a single Jupyter kernel; prefer launching via terminal/HPC batch or a Tapis‑based workflow for multi‑process jobs.


