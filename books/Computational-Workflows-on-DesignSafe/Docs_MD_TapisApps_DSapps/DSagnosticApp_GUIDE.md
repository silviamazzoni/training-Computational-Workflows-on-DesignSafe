#  AgnosticApp - How to Choose Inputs

***A One-Page Cheat Sheet for *designsafe-agnostic-app****

This app gives you a lot of power. You do **not** need to use most inputs for most jobs.

Use this page to answer **four questions**, top to bottom.

---

## 1. What am I actually running?

Pick **one executable** and **one main script**.

| If you are running…     | Set *BINARYNAME*             | Set *INPUTSCRIPT* |
| ----------------------- | ---------------------------- | ----------------- |
| OpenSees (Tcl)          | *OpenSees*                   | *model.tcl*       |
| OpenSeesMP / OpenSeesSP | *OpenSeesMP* or *OpenSeesSP* | *model.tcl*       |
| OpenSeesPy              | *python3*                    | *run.py*          |
| General Python          | *python3*                    | *script.py*       |
| Other executable        | *<binary name>*              | *script*          |

**Rules of thumb**

* *INPUTSCRIPT* is **just the filename**, not a path
* The script **must live inside *inputDirectory***
* For OpenSeesPy, **always use *python3***

---

## 2. Do I need MPI?

Answer this **explicitly** — the app will not guess.

| If your job…                                              | Set *UseMPI* |
| --------------------------------------------------------- | ------------ |
| Uses OpenSeesMP / OpenSeesSP                              | *True*       |
| Uses *mpi4py*                                             | *True*       |
| Is fully serial                                           | *False*      |
| Uses Python threading or *concurrent.futures* on one node | *False*      |

**Mental model**

```text
UseMPI = True   →  ibrun <command>
UseMPI = False  →  <command>
```

If you’re unsure:
 **start with *False*** and turn it on only when needed.

---

## 3. Does my environment need anything special?

### A. Do I need modules?

If your code needs:

* OpenSees
* MPI-aware HDF5
* a specific compiler stack

 **Yes, you need modules**

Choose **one**:

| Use this when…                      | Input               |
| ----------------------------------- | ------------------- |
| You want a clean, documented stack  | *MODULE_LOADS_FILE* |
| You just need a few modules quickly | *MODULE_LOADS_LIST* |

Example mental model:

```text
If I would type “module load …” on the command line,
I probably need to declare it here.
```

---

### B. Do I need Python packages?

| If you…                        | Use                 |
| ------------------------------ | ------------------- |
| Have a *requirements.txt*      | *PIP_INSTALLS_FILE* |
| Just need a couple of packages | *PIP_INSTALLS_LIST* |
| Need none                      | *(leave blank)*     |

Packages are installed **inside the job only**.

---

### C. Am I using OpenSeesPy?

 **Almost always set this to True on Stampede3**

```text
GET_TACC_OPENSEESPY = True
```

Why:

* Uses the **TACC-compiled OpenSeesPy.so**
* Avoids broken or incompatible PyPI wheels

---

## 4 How are my inputs structured?

### A. Is everything already in my input directory?

If yes:

* do nothing
* simplest and safest case

---

### B. Do I have ZIP bundles?

Use when:

* many small files
* datasets packaged for upload

--> Set:

```text
UNZIP_FILES_LIST = mydata,meshes
```

(*.zip* is optional)

---

### C. Do I need large external data?

Use when:

* data already exists in WORK / SCRATCH / HOME
* you don’t want to re-upload it

--> Set:

```text
PATH_COPY_IN_LIST = /work/.../dataset1,/scratch/.../dataset2
```

If the copy is **temporary**, also set:

```text
DELETE_COPIED_IN_ON_EXIT = True
```

---

## 5. Do I need pre- or post-processing?

| Need                 | Input             |
| -------------------- | ----------------- |
| Generate inputs      | *PRE_JOB_SCRIPT*  |
| Post-process results | *POST_JOB_SCRIPT* |
| Organize outputs     | *POST_JOB_SCRIPT* |
| Cleanup              | *POST_JOB_SCRIPT* |

Hooks:

* run **inside *inputDirectory***
* may be executable or run via *bash*
* failures warn by default (job continues)

---

## 6. Will my output be large or long-lived?

### A. Many output files?

--> Enable ZIP repack:

```text
ZIP_OUTPUT_SWITCH = True
```

---

### B. Do I want results in WORK or SCRATCH immediately?

--> Move outputs:

```text
PATH_MOVE_OUTPUT = $WORK/MyRuns
```

Results land in:

```text
$WORK/MyRuns/_<JobUUID>/
```

This is **highly recommended** for:

* large runs
* chained workflows
* interactive inspection in JupyterHub

---

## 7. Minimal “starter configurations”

### * Serial OpenSees (Tcl)

```text
BINARYNAME   = OpenSees
INPUTSCRIPT = model.tcl
UseMPI      = False
```

---

### * OpenSeesMP (MPI)

```text
BINARYNAME   = OpenSeesMP
INPUTSCRIPT = model.tcl
UseMPI      = True
```

---

### * OpenSeesPy (recommended default)

```text
BINARYNAME            = python3
INPUTSCRIPT          = run.py
UseMPI               = False
GET_TACC_OPENSEESPY  = True
```

---

### * Python + mpi4py

```text
BINARYNAME   = python3
INPUTSCRIPT = run.py
UseMPI      = True
PIP_INSTALLS_LIST = mpi4py
```

---

## 8. Final sanity checklist

Before submitting, ask yourself:

*  Is my script inside *inputDirectory*?
*  Does *UseMPI* match how I actually run the code?
*  Do my modules match my binary?
*  Am I relying on any absolute paths unintentionally?
*  Do I want outputs zipped or moved?

If yes → you’re good.

---

###  One-sentence takeaway

**Choose the simplest inputs that describe how you would run the job manually — the app exists to make that behavior explicit, safe, and reproducible.**

