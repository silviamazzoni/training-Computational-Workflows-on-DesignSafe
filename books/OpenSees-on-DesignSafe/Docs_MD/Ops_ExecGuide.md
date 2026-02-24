# Execution Guide
**Summary: Choosing the Right Execution Strategy**

Selecting the appropriate execution mode and parallel strategy depends on the scale of your model, the type of study you're conducting, and your computing environment.

## Quick Reference Table

| Use Case                       | Mode                      | Example Command                        | Notes                                                  |
| ------------------------------ | ------------------------- | -------------------------------------- | ------------------------------------------------------ |
| Exploring commands             | Interactive               | *OpenSees* or *python*                 | Best in terminal or small scripts                      |
| Full analysis run (sequential) | Non-Interactive           | *OpenSees model.tcl*                   | Most common for local or small batch jobs              |
| Batch run with varying inputs  | Arg-based Non-Interactive | *OpenSees model.tcl 0.05 10 input.at2* | Great for sweeps, job arrays                           |
| Parallel simulation (Tcl)      | MPI via OpenSeesMP/SP     | *mpiexec -np 4 OpenSeesMP model.tcl*   | Choose MP or SP based on domain decomposition style    |
| Parallel simulation (Python)   | MPI via OpenSeesPy        | *mpiexec -np 4 python model.py*        | Supports OpenSeesMP-style decomposition internally     |
| Independent jobs (Python)      | concurrent.futures        | *ProcessPoolExecutor(...).map(...)*    | For embarrassingly parallel jobs without communication |

## Decision Flow

1. **Do you need multiple processes or distributed memory?**

   * ✅ Yes → Use **MPI** with *OpenSeesMP* or *OpenSeesPy*
   * ❌ No → Continue

2. **Do you want to vary inputs across runs?**

   * ✅ Yes → Use **command-line arguments** and loop/array strategy
   * ❌ No → Run script directly (non-interactive)

3. **Are jobs independent (no MPI communication)?**

   * ✅ Yes → Use *concurrent.futures* in Python for batch submission
   * ❌ No → Stick with *mpiexec* and an MPI-based script

4. **Running in DesignSafe Jupyter?**

   * Use terminal to launch parallel jobs
   * Submit to Tapis or HPC cluster for large-scale runs

With these strategies and tools, you can scale from small test scripts to full-scale simulations across hundreds of processors—without rewriting your core model.

## Debugging and Monitoring Tips

* Use **print** or **puts** statements to identify which process is active
* Check Slurm **.out**/**.err** files or use **squeue** to monitor job status when logged into a login node on the HPC
* Use Tapis job history panel or **t.jobs.getJobStatus()** to track progress
* In OpenSeesMP and OpenSeesSP:
  * use **getPID** and **getNP**
* In Python:
  * Get rank with **ops.getPID()** or **MPI.COMM_WORLD.Get_rank()**
  * Use **os.getcwd()** and **os.listdir()** to inspect files during execution
