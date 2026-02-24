# Parallel Execution: ibrun
***Parallel Execution in SLURM: Using ibrun***

When running jobs on **Stampede3** or other TACC HPC systems via **SLURM**, you must use ***ibrun* instead of *mpiexec***.

*ibrun* is a TACC-specific MPI launcher that ensures your parallel processes are correctly scheduled and distributed across allocated cores and nodes.

## Replace *mpiexec* with *ibrun* in SLURM Scripts

| Context          | Command Example              |
| ---------------- | ---------------------------- |
| Tcl (OpenSeesMP) | ibrun OpenSeesMP model.tcl |
| Tcl (OpenSeesSP) | ibrun OpenSeesSP model.tcl |
| OpenSeesPy       | ibrun python model.py      |

> This applies inside your *job.slurm* or *tapisjob_app.sh* batch script — not in the terminal or Jupyter.

## Example SLURM Script Snippet

:::{dropdown} Tcl
```bash
#SBATCH -N 2               # 2 nodes
#SBATCH -n 56              # 56 total MPI processes (e.g., 28 per node)
#SBATCH -t 00:30:00        # Wall time

# module load intelmpi
module load hdf5/1.14.4
module load opensees

ibrun OpenSeesMP model.tcl 3 5 input.at2
```
NOTE: No need to load the *intelmpi* module, the opensees module has it as a dependency and will load it as part of its environment stack.

**Only Load *intelmpi* Manually If**:
* You’re compiling your own MPI program.
* You’re running a non-OpenSees MPI application.
* You need to test MPI behavior independent of OpenSees.

:::

:::{dropdown} Python:
    
```bash
#SBATCH -N 2               # 2 nodes
#SBATCH -n 56              # 56 total MPI processes (e.g., 28 per node)
#SBATCH -t 00:30:00        # Wall time

# install what is needed...

ibrun python model.py --model 2 --output results/
```
:::
## Why *ibrun*?

* *ibrun* is required by TACC to launch MPI programs in batch jobs
* It works with TACC’s SLURM scheduler, job environment, and MPI configuration.
* It ensures correct core placement and resource binding
* It ensures MPI ranks are mapped correctly to cores/nodes.
* *mpiexec* might run but produce incorrect or inefficient results on TACC systems.

## Number of MPI processes in *ibrun*
When using ibrun inside a SLURM job, you don’t explicitly specify the number of processes in the ibrun command. Instead, you allocate the number of MPI processes using the SLURM directives in your job script, and ibrun automatically launches one MPI process per allocated core.


### Step-by-Step: Allocating MPI Processes with *ibrun*

:::{dropdown} 1. Specify your allocation in the SLURM script:
    
```bash
#SBATCH -N 2              # Number of nodes
#SBATCH -n 56             # Total MPI tasks (e.g., 28 per node)
#SBATCH -t 00:30:00       # Wall time
```

* *-N* sets the number of nodes.
* *-n* sets the total number of **MPI ranks** (processes) to be launched by *ibrun*.

> ⚠️ Stampede3 nodes typically have **56 cores**, so *-n 56* will use 1 full node; *-n 112* uses 2 nodes.

:::

:::{dropdown} 2. Run your command with *ibrun* — no need to specify *-np*
    
```bash
ibrun OpenSeesMP model.tcl
```

or for OpenSeesPy:

```bash
ibrun python model.py
```

> *ibrun* automatically uses the number of MPI ranks you requested with *#SBATCH -n*.

:::

:::{dropdown} Bonus: Controlling MPI Task Placement *(Advanced)*

If needed, you can use SLURM’s *--ntasks-per-node* or *--cpus-per-task* options to fine-tune placement:

```bash
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH -n 56
```

This launches 28 MPI tasks per node, for 2 nodes = 56 total tasks.

:::


### Full Example Job Script for OpenSeesMP

```bash
#!/bin/bash
#SBATCH -J opensees-job
#SBATCH -o output.%j.out
#SBATCH -e output.%j.err
#SBATCH -N 2
#SBATCH -n 56
#SBATCH -t 00:20:00

module load intelmpi
module load opensees

ibrun OpenSeesMP model.tcl 3 5 input.at2
```






## Summary

| Platform              | MPI Launcher | Use Case              |
| --------------------- | ------------ | --------------------- |
| JupyterHub (Terminal) | mpiexec    | Testing / Prototyping |
| Stampede3 (SLURM)     | ibrun      | HPC Production Jobs   |

```{admonition} Key Notes
* Always use ibrun for parallel jobs on Stampede3
* Use mpiexec only in interactive terminals (Jupyter, local)
* Combine command-line arguments with parallel execution to enable large-scale studies
* Both Tcl and Python can be used flexibly in job arrays, automation scripts, or parameter sweeps
```