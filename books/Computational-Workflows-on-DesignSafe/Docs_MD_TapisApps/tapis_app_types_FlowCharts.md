# Execution Flows
***Diagrams Showing ZIP vs. Singularity Execution Flows***

*(ASCII diagrams, clean, readable, works in Markdown and HTML environments)*

You can place these in your *Tapis Apps Overview* section as visual explanations.

---

## ZIP Runtime Execution Flow

**Lightweight • Uses Host Environment • Leverages TACC Modules**

```
          ┌──────────────────────────┐
          │        User Job          │
          │   (inputs + parameters)  │
          └─────────────┬────────────┘
                        │
                        ▼
              Tapis Stages Inputs
        (all files placed in job directory)
                        │
                        ▼
            ┌─────────────────────────┐
            │  Copy ZIP archive into  │
            │  execSystemExecDir      │
            └─────────────┬───────────┘
                          │
                          ▼
                Unpack ZIP Archive
      (scripts, wrappers, configs, run files)
                          │
                          ▼
        Load TACC Modules (e.g., OpenSeesMP,
           MPI, HDF5, Python, etc.)
                          │
                          ▼
           Tapis Constructs Launch Script
                (Slurm batch script)
                          │
                          ▼
               Slurm Schedules Job
                          │
                          ▼
        Host Executes Script Directly
   (no container — code runs inside HPC environment)
                          │
                          ▼
            Outputs Collected by Tapis
```

**Mental model:**
ZIP = *“Unpack → Use modules → Run script directly on Stampede3/Frontera.”*

---

## Singularity / Apptainer Runtime Execution Flow

**Self-Contained • Reproducible • Custom Environments**

```
          ┌──────────────────────────┐
          │        User Job          │
          │   (inputs + parameters)  │
          └─────────────┬────────────┘
                        │
                        ▼
              Tapis Stages Inputs
        (all files placed in job directory)
                        │
                        ▼
       Singularity Image (.sif) Located
     (local path or copied into exec dir)
                        │
                        ▼
           Tapis Constructs Launch Script
          (typically includes a command like)
      →  apptainer run image.sif <arguments>
                        │
                        ▼
               Slurm Schedules Job
                        │
                        ▼
     Singularity Container Starts on Node
     (binds input/output directories inside)
                        │
                        ▼
       Executable Runs *inside the container*
      (full environment defined by the .sif)
                        │
                        ▼
            Outputs Collected by Tapis
```

**Mental model:**
Singularity = *“Start container → Bind job dirs → Execute inside container.”*

---

## ZIP vs. Singularity: Side-by-Side (Mini Diagram)

```
ZIP Runtime                          Singularity Runtime
--------------                      -----------------------
Unpack ZIP → use system modules →   Bind dirs → start container →
run script directly                 run executable inside image
```
