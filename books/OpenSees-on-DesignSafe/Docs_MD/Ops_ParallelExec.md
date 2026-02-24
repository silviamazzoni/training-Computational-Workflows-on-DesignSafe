# Parallel Execution
**MPI and *ibrun*: Parallel Execution on HPC Systems**

OpenSees supports parallel execution through **MPI (Message Passing Interface)**, a widely used protocol that allows multiple processes to work together across processors or nodes in a high-performance computing (HPC) environment. MPI enables large structural simulations to be split into smaller tasks and solved concurrently, greatly improving performance and scalability. 
* On TACC systems like **Stampede3**, MPI programs must be launched using **ibrun**—a system-specific command that ensures MPI processes are correctly assigned to the compute resources allocated by SLURM.
* While **mpiexec** is suitable for interactive environments like JupyterHub, **ibrun is required in batch jobs** on Stampede3 to ensure proper task placement, resource binding, and compatibility with the system’s MPI stack.
