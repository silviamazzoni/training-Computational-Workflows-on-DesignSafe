# How to Run a SLURM Job
***Run a SLURM Job on Stampede3***

You can run applications on TACC’s **Stampede3** system by submitting a **SLURM batch job script**. This method gives you direct, low-level control over how your simulations execute — ideal for advanced users managing many simultaneous runs, optimizing memory or MPI settings, or coordinating multiple software packages.

## Example: SLURM Script for Python
    
Here’s a typical SLURM batch script (*job.slurm*) that runs OpenSeesMP on **64 cores across 2 nodes**:

```bash
#!/bin/bash
#SBATCH -J MyOpenSeesJob
#SBATCH -o output.%j.out
#SBATCH -e output.%j.err
#SBATCH -p normal
#SBATCH -N 2
#SBATCH -n 64
#SBATCH -t 02:00:00

module load python/3.xx


cd $SCRATCH/myproject
ibrun python PythonMPI.py
```

**Explanation:**

* *#SBATCH* lines set job metadata: name, output files, partition, nodes, core count, and time.
* *module load* activates compilers and software.
* *cd* changes to your project directory on **\$SCRATCH**.
* *ibrun* launches the parallel MPI job using TACC’s launcher.

## Why Run on *$SCRATCH*?
    
*$SCRATCH* is a **high-speed parallel file system** for compute jobs. Always:

1. Copy inputs to *$SCRATCH* (*cp* or *rsync*).
2. Run your job **from there**.
3. Copy results back to *$WORK* or *$HOME* after completion.

Running on *$SCRATCH* ensures performance and prevents I/O bottlenecks. This is what DesignSafe apps do behind the scenes.
    
    
## Steps
    
1. **Prepare and Submit Your Job**

```bash
# Log into Stampede3
ssh username@stampede.tacc.utexas.edu

# Create and populate your scratch project directory
mkdir -p $SCRATCH/myproject
cp mymodel.tcl job.slurm $SCRATCH/myproject
cd $SCRATCH/myproject

# Submit the job
sbatch job.slurm
```

2. **Monitor and Manage**

```bash
# View your queued and running jobs
squeue -u $USER

# Cancel a job
scancel <job_id>

# View more details after completion
sacct -j <job_id>
```
    
    
## Execution Tips
    
**Check Job Output**

* **.o<jobid>* = standard output (*stdout*)
* **.e<jobid>* = standard error (*stderr*)
* These files help debug failed jobs.

##  Job Types

* **MPI jobs**:

  ```bash
  ibrun ./my_mpi_program
  ```
* **Serial / Python**:

  ```bash
  python my_script.py
  ```
* **OpenMP / Hybrid**:

  ```bash
  export OMP_NUM_THREADS=4
  ./my_openmp_program
  ```
    
    
## SLURM Tools and Commands
    
| Command            | Description                            |
| ------------------ | -------------------------------------- |
| *sbatch job.slurm* | Submit a job                           |
| *squeue -u $USER*  | View all jobs submitted by your user   |
| *squeue -j JOBID*  | Check job details                      |
| *scancel JOBID*    | Cancel a job                           |
| *sacct -j JOBID*   | See accounting info after job finishes |
| *sinfo*            | View available partitions and nodes    |
    
    
    
## Helpful Tips
    
* **Start small** using the *development* queue:

  ```bash
  #SBATCH -p development
  #SBATCH -t 00:30:00
  ```

* **Use interactive dev sessions** to debug jobs:

  ```bash
  idev -N 1 -n 64 -p development -t 00:30:00
  ```

* **Make sure your script is executable:**

  ```bash
  chmod +x job.slurm
  ```

* **Check available software:**

  ```bash
  module avail
  module spider
  ```

* **Using Conda? Activate your environment:**

  ```bash
  module load python3
  source activate myenv
  ```



## Summary

* Use SLURM scripts to run batch jobs on Stampede3.
* Place your working files in *$SCRATCH* for best performance.
* Use *ibrun* for MPI programs like OpenSeesMP.
* Monitor jobs with *squeue*, debug with **.out* and **.err*.
* Start with test runs in the development queue, then scale.

