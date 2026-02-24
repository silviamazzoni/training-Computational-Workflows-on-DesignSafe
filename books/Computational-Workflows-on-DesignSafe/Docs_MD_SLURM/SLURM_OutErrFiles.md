# SLURM-Job Output
***Reading '.out' and '.err' Files -- critical for debugging***

When you submit a SLURM job using:

```bash
sbatch job.slurm
```

SLURM automatically captures your program’s output in two key files:

| File                 | Description                                                                                    |
| -------------------- | ---------------------------------------------------------------------------------------------- |
| *output.<jobid>.out* | Captures **standard output** — anything your script prints via *print*, *puts*, stdout, or from the solver.     |
| *output.<jobid>.err* | Captures **standard error** — runtime errors, syntax issues, missing files, MPI problems, etc. |


These files are automatically named using the job ID and should be your **first stop when debugging** a failed or stalled job.

## Example

You will find the output files in the base folder of where your SLURM job was executed, or tranferred to.

### What to Look For
* ***.out* – Standard Output**

    This file logs the **normal progress** of your job, such as:
    
    * Echoed input parameters or timestamps
    * Printed results or summaries
    * Completion messages from OpenSees or your script
    * Debugging output you inserted (e.g., *print("step 1 done")*)
    
    If this file is **empty**, it might mean your script failed very early, before any standard output was produced.

* ***.err* – Standard Error**

    This file contains **critical diagnostics**:
    
    * Tcl or Python syntax errors
    * Missing or misnamed input files
    * Failed module loads (e.g., a missing OpenSees executable)
    * MPI startup issues (*OpenSeesSP* or *OpenSeesMP*)
    * Permission problems (e.g., trying to write to a read-only directory)
    
    Even if your job produced output, always check the *.err* file — it may reveal **warnings** or **silent failures** that don't stop the job but indicate something went wrong.
    
## Best Practice

Always check both files after a job finishes (or fails). These files files are stored with your input script. You can view them in JupyterHub or the Data Depot, which you'd access from the Job-Status page.


In most cases, they will tell you **exactly what went wrong**, or confirm that your job completed successfully.

If you're debugging an OpenSees model, this is where you'll find:

* The stack trace of a failed script
* Errors about file paths, mesh loading, or convergence issues
* Output from *puts* or *print* statements that help trace execution



:::{dropdown} Failed Job Example

Check the files:

* *```xx.err*:

    ```
    mpirun: error: unable to open hostfile: No such file or directory
    ERROR: MPI process failed to start
    child process exited abnormally
    ```

* *```x.out*:

    ```
    <empty>
    ```

* **Diagnosis:**
    MPI tried to launch *OpenSeesSP* but couldn't find the required hostfile. This typically happens when:
    
    * You didn’t request multiple nodes but your environment needs one
    * Your *mpirun* configuration doesn’t match the scheduler
    * OpenSees isn’t correctly installed or loaded
:::

## Troubleshooting Checklist

Use this list when your SLURM job doesn’t behave as expected:

|  Step | What to Check                                                    | File            |
| ------ | ---------------------------------------------------------------- | --------------- |
| 1      | Did the job run at all? Look for start/stop messages.            | *.out*          |
| 2      | Is there a syntax or runtime error?                              | *.err*          |
| 3      | Any missing input files or path typos?                           | *.err*          |
| 4      | Are MPI commands/formats correct?                                | *.err*          |
| 5      | Are you using the correct executable (*OpenSees*, *OpenSeesSP*)? | *.out* / *.err* |
| 6      | Does the output stop partway through? Check for crashes.         | *.out* / *.err* |
| 7      | Does your script use absolute or relative paths?                 | Both            |
| 8      | Is there a SLURM-specific error (e.g., exceeded time limit)?     | *.err*          |

```{tip}
* **Empty *.out* file?** Your job likely failed before any output was printed.
* **Empty *.err* file?** Great! But check *.out* for unexpected early exits.
* **Still unsure?** Insert *puts "Starting..."* or *print("Reached step 2")* to help trace the point of failure.
```
