# AgnosticApp - Quick Reference

This table defines **all user-facing inputs and environment variables** supported by the app.
Details and relationships are explained in later sections.

### Core Execution Inputs

| Input            | Required | Description                                                                 |
| ---------------- | -------- | --------------------------------------------------------------------------- |
| **inputDirectory** | ✔        | Directory containing the main script and all runtime files                  |
| **BINARYNAME**     | ✔        | Executable to run (*OpenSees*, *OpenSeesMP*, *OpenSeesSP*, *python3*, etc.) |
| **INPUTSCRIPT**    | ✔        | Main script filename inside *inputDirectory*                                |
| **UseMPI**         | ✔        | Whether to launch with *ibrun* (MPI)                                        |

---

### Command-Line Arguments

| Input       | Required | Description                                                |
| ----------- | -------- | ---------------------------------------------------------- |
| **ARGUMENTS** | ✖        | Free-form command-line arguments appended after the script |

---

### Module & Environment Configuration

| Input               | Required | Description                                                        |
| ------------------- | -------- | ------------------------------------------------------------------ |
| **MODULE_LOADS_LIST** | ✖        | Comma-separated list of modules to load                            |
| **MODULE_LOADS_FILE** | ✖        | File listing modules to load |

---

### Python Package Management

| Input               | Required | Description                                     |
| ------------------- | -------- | ----------------------------------------------- |
| **PIP_INSTALLS_LIST** | ✖        | Comma-separated list of pip packages to install |
| **PIP_INSTALLS_FILE** | ✖        | *requirements.txt*-style file                   |

---

### OpenSees / OpenSeesPy Support

| Input                 | Required | Description                                           |
| --------------------- | -------- | ----------------------------------------------------- |
| **GET_TACC_OPENSEESPY** | ✖        | Copy TACC-compiled *OpenSeesPy.so* into run directory |

---

### Input Staging & Preparation

| Input                      | Required | Description                                   |
| -------------------------- | -------- | --------------------------------------------- |
| **UNZIP_FILES_LIST**         | ✖        | ZIP files in *inputDirectory* to expand       |
| **PATH_COPY_IN_LIST**        | ✖        | Absolute paths (WORK/SCRATCH/HOME) to copy in |
| **DELETE_COPIED_IN_ON_EXIT** | ✖        | Remove copied-in paths after job completes    |

---

### Pre/Post Execution Hooks

| Input             | Required | Description                          |
| ----------------- | -------- | ------------------------------------ |
| **PRE_JOB_SCRIPT**  | ✖        | Script to run before main executable |
| **POST_JOB_SCRIPT** | ✖        | Script to run after main executable  |

---

### Output Management

| Input               | Required | Description                            |
| ------------------- | -------- | -------------------------------------- |
| **ZIP_OUTPUT_SWITCH** | ✖        | Repack output directory into a ZIP     |
| **PATH_MOVE_OUTPUT**  | ✖        | Move final output to WORK/SCRATCH/HOME |
