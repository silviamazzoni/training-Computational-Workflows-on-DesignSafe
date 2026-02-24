# AgnosticApp - Input Arguments
***Input parameters (what each one means)***

This section is the “user manual” for every input you see in the portal.

## 1. File input

### **Input Directory** (required)
**What it is:** A *single directory* staged by Tapis into the job.  
**What should be inside:**
- your main script (Tcl or Python)
- any supporting files your script needs (models, data, configs)
- optional helper files:
  - *modules.txt* (for *MODULE_LOADS_FILE*)
  - *requirements.txt* (for *PIP_INSTALLS_FILE*)
  - *prehook.sh* / *posthook.sh* (for hook variables)
  - zipped bundles referenced by *UNZIP_FILES_LIST*

**Runtime behavior:** The wrapper *cd*s into this directory before running the main command.  
**Implication:** relative paths in your script should assume this directory is the working directory.

---

## 2. Required app arguments

### **Main Program** (required)
**What it is:** The executable to run (binary name).  
**Common values:**
- *OpenSees* (serial Tcl)
- *OpenSeesMP* / *OpenSeesSP* (MPI Tcl)
- *python3* (Python workflows, including OpenSeesPy)

**Where it must come from:**
- available via modules (recommended), or
- present in the working directory / PATH

**Wrapper notes:**
- If *Main Program* is *python* or *python3*, the wrapper normalizes to *python3*.

---

### **Main Script** (required)
**What it is:** The filename of the input script passed to the executable.  
**Rules:**
- filename only (no path)
- must exist inside the **Input Directory**

Examples:
- *model.tcl*
- *run_analysis.py*
- *Ex1a.Canti2D.Push.argv.tacc.py*

---

### **UseMPI** (required)
Controls whether the wrapper launches the executable through *ibrun*.

| UseMPI value | What runs |
|---|---|
| *False* | *<Main Program> <Main Script> [args...]* |
| *True*  | *ibrun <Main Program> <Main Script> [args...]* |

**Use *True* when:**
- OpenSeesMP / OpenSeesSP
- Python + *mpi4py*

**Use *False* when:**
- serial OpenSees (Tcl)
- serial Python / OpenSeesPy
- Python using threading / *concurrent.futures* within a node

> Note: the wrapper treats many “true-like” values as True (*True*, *1*, *Yes*, case-insensitive).

---

### **CommandLine Arguments** (optional)
Free-form arguments appended after the Main Script.

Example:
```text
--NodalMass 4.19 --outDir outCase1
```

Final command structure:
```bash
[ibrun] <MainProgram> <MainScript> <Arguments...>
```

---

## 3. Scheduler inputs

### **TACC Scheduler Profile** (defaulted)
The app uses the *tacc-no-modules* profile by default so **no modules are implicitly loaded**.
This is intentional: module state is controlled explicitly by the wrapper to improve reproducibility.

### **TACC Reservation** (optional)
Provide a reservation string if you have one.

---

## 4. Environment variables (advanced configuration)

These values are presented as app inputs in the portal. Most are optional. If you never set them, the wrapper runs with conservative defaults.

### 4.1 OpenSeesPy injection

#### **GET_TACC_OPENSEESPY** (default: *True*)
If True-like, the wrapper attempts to use the **TACC-compiled OpenSeesPy** by:
- loading *python/3.12.11*, *hdf5/1.14.4*, *opensees*
- copying *${TACC_OPENSEES_BIN}/OpenSeesPy.so* into the working directory as *./opensees.so*

**Use this when:**
- you want reliable OpenSeesPy on Stampede3 (recommended)

**In your Python script:**
```python
import opensees as ops
```

**Notes / failure modes:**
- if *TACC_OPENSEES_BIN* is unset or *OpenSeesPy.so* is missing, the wrapper logs a warning and skips the copy.

---

### 4.2 Module loading (two mechanisms)
The two mechanisms are complementary -- you can use both.

#### A. **MODULE_LOADS_FILE** (optional)
A filename (in the Input Directory) containing module commands, one per line.

Supported line formats:
- *purge*
- *use <path>*
- *load <module>*
- *?module* (optional *try-load*)
- bare module names

This is best for **version-controlled, documented module stacks**. It also makes submittal via the web-portal interface easier.

#### B. **MODULE_LOADS_LIST** (optional)
Comma-separated list of modules to load, e.g.:
```text
python/3.12.11,opensees,hdf5/1.14.4,pylauncher
```

**Tip:** use *MODULE_LOADS_FILE* when the setup is more than a few modules or needs comments.

---

### 4.3 Python package installs (two mechanisms)
The two mechanisms are complementary -- you can use both.

#### A. **PIP_INSTALLS_FILE** (optional)
A requirements-style file (in the Input Directory), e.g. *requirements.txt*.

Wrapper behavior:
- runs *pip3 install -r <file>*
- fails the job if pip fails (with a clear error)

It makes submittal via the web-portal interface easier.

#### B. **PIP_INSTALLS_LIST** (optional)
Comma-separated list of packages, e.g.:
```text
mpi4py,pandas,numpy,matplotlib
```

Wrapper behavior:
- installs each package with *pip3 install <pkg>*
- fails the job if any install fails

---

### 4.4 Input preparation

#### A. **UNZIP_FILES_LIST** (optional)
Comma-separated list of ZIP files *in the Input Directory* to expand before execution.
Entries may omit the *.zip* suffix.

Use this when:
- you staged one bundled zip instead of many small files

#### B. **PATH_COPY_IN_LIST** (optional)
Comma-separated list of **absolute paths** (within the execution system) to copy into the working directory before execution.

Example:
```text
$WORK/FileSet2,$SCRATCH/FileSet3/thisFile.at2
```

Use this when:
- you need large/shared datasets without duplicating them into the Input Directory
- you want a specific runtime layout inside the working directory

#### C. **DELETE_COPIED_IN_ON_EXIT** (default: *0*)
If set to *1* / True-like, the wrapper deletes only the copied-in items listed in its manifest on exit.

Safety rules:
- refuses absolute paths
- refuses *..* traversal
- deletes only what landed in the working directory

Use this when:
- copy-in files are “temporary conveniences” and should not be archived

---

### 4.5 Pre/Post hooks

#### A. **PRE_JOB_SCRIPT** (optional)
Script to run after environment setup but before the main executable.
- if relative, interpreted as *./script* inside the Input Directory
- if executable, run directly; otherwise run via *bash*

#### B. **POST_JOB_SCRIPT** (optional)
Script to run after the main executable (same resolution rules as pre-hook).

**Default policy:** hook failures are logged as warnings and the job continues (you can change this policy in the wrapper if desired).

---

### 4.6 Output management

#### A. **ZIP_OUTPUT_SWITCH** (default: *False*)
If True-like:
- zips the entire Input Directory after execution into *inputDirectory.zip*
- removes the original directory

Use this when:
- output is large and contains many small files
- you want a single artifact to move / download

#### B. **PATH_MOVE_OUTPUT** (optional)
If set, the wrapper moves the main output artifact into:
```text
<PATH_MOVE_OUTPUT>/_<JobUUID>/
```
and copies top-level logs into that same folder.

Recommended:
- move to *$WORK/...* for interactive inspection in JupyterHub
- move to *$SCRATCH/...* for chained HPC workflows


---

## 5. Typical patterns

### Serial OpenSees (Tcl)
- Main Program: *OpenSees*
- UseMPI: *False*

### OpenSeesMP / OpenSeesSP (MPI)
- Main Program: *OpenSeesMP* (or *OpenSeesSP*)
- UseMPI: *True*

### OpenSeesPy (serial)
- Main Program: *python3*
- UseMPI: *False*
- *GET_TACC_OPENSEESPY=True*

### Python + mpi4py
- Main Program: *python3*
- UseMPI: *True*
- *PIP_INSTALLS_LIST=mpi4py* (or requirements file)


