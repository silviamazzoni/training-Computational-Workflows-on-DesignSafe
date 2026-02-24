# Scheduler- vs Script-Launched MPI

In a Tapis app, **two *jobAttributes* fields control how MPI starts**:

* *isMpi* — whether the scheduler launches your job under MPI.
* *mpiCmd* — the site launcher (e.g., *"ibrun"* on Stampede3) **used only when** *isMpi* is *true*.

**Pick a mode up front:**

* Use ***isMpi: true* + *mpiCmd: "ibrun"*** when you want SLURM/Tapis to wrap the **entire job** in MPI (your script runs on all ranks from line 1).
* Use ***isMpi: false* + *mpiCmd: null*** when you want a **serial script** that you selectively parallelize by calling *ibrun* yourself where needed.

> **Schema tip:** If *isMpi* is *false*, *mpiCmd* must be ***null*** (not an empty string). If *isMpi* is *true*, *mpiCmd* must be a **non-empty** string.

---

## Scheduler-launched MPI

* **Who starts MPI?** SLURM/Tapis wraps the whole job with the launcher.
* **app.json:** *"isMpi": true*, *"mpiCmd": "ibrun"*.
* **How your script runs:** *tapisjob_app.sh* starts on **all ranks**; do **not** call *ibrun* inside.
* **When it shines:** Whole workflow is parallel; minimal serial work.
* **Gotchas:** Guard one-time actions (*if rank==0:*). Easy to “double-wrap” by calling *ibrun* inside an MPI job—don’t.

---

## Script-launched MPI *(recommended for the tester)*

* **Who starts MPI?** Your script invokes the launcher only where needed.
* **app.json:** *"isMpi": false*, *"mpiCmd": null*.
* **How your script runs:** Serial by default; explicitly use *ibrun* only for MPI steps.
* **When it shines:** Mixed serial + small MPI sections (e.g., quick *mpi4py* hello). Safer for one-time installs (e.g., building *mpi4py*) without race conditions.

---

## Minimal configs

**Scheduler-launched (MPI everywhere)**

```json
"isMpi": true,
"mpiCmd": "ibrun"
```

```bash
# Already on ALL ranks; do not call ibrun here
"$MEXE" run -p "$ENV_DIR" python -m mpi4py your_program.py
# Guard one-time prints/writes
"$MEXE" run -p "$ENV_DIR" python - <<'PY'
from mpi4py import MPI
if MPI.COMM_WORLD.rank == 0:
    print("one-time summary")
PY
```

**Script-launched (MPI only where needed)**

```json
"isMpi": false,
"mpiCmd": null
```

```bash
# Serial checks
"$MEXE" run -p "$ENV_DIR" python -V
# MPI just here
ibrun "$MEXE" run -p "$ENV_DIR" python -m mpi4py _mpi_hello.py
```

---

## Quick decision guide

* Choose **scheduler-launched** if your job is MPI end-to-end and you’re already guarding I/O.
* Choose **script-launched** for environment checks, version asserts, selective MPI calls, and one-time installs like *mpi4py*.
