# Parallel Execution: MPI
***Parallel Execution with MPI in OpenSees-Tcl and OpenSeesPy***
    
Parallel computing is essential for solving large structural models efficiently. 

OpenSees supports parallel computing through **MPI (Message Passing Interface)**, a standardized communication protocol used in high-performance computing (HPC) to run tasks across multiple processors or nodes. MPI enables multiple processes to run simultaneously and exchange data during execution, allowing large simulations to be distributed and executed more efficiently.

MPI has been pre-installed in the JupyterHub as well as Stempede3, so no additional setup is required to run parallel OpenSees jobs.

## What is MPI?
MPI (Message Passing Interface) is a widely used standard for parallel programming in distributed-memory systems. It allows multiple computing processes—often on different nodes of an HPC cluster—to communicate by sending and receiving messages.

In OpenSees, MPI enables large structural models to be divided and solved concurrently across multiple processors, significantly reducing simulation time.

To run **parallel versions**, you use the *mpiexec* command to launch the Application and specify the number of processors (N) using the inputFile.


:::{dropdown} Tcl-Based Parallel Execution
 The Tcl-based OpenSees applications—OpenSees, OpenSeesSP, and OpenSeesMP—are compiled executables written in C++. These programs are run directly from the command line and do not rely on an interpreter once compiled.

| Executable   | Purpose                                 | Run | Supports MPI |
| ------------ | --------------------------------------- | --- | -------------|
| *OpenSees*   | Serial execution                        | Single Process | NO |
| *OpenSeesSP* | Domain decomposition (1 model per core) | Single Process per Domain Decomposition | YES |
| *OpenSeesMP* | Element decomposition (shared model)    | Multiple Processes per Element Decomposition | YES |


When you launch one of these in parallel using MPI, such as:
```
mpiexec -np 4 OpenSeesMP model.tcl
```
**MPI** starts 4 separate processes, each running the same executable. These processes communicate and synchronize via MPI to divide the workload (e.g., mesh partitions, domain decomposition) and solve the model in parallel.
:::

:::{dropdown} Python-Based Parallel Execution (OpenSeesPy)

OpenSeesPy is a **Python** wrapper around the OpenSees C++ engine and provides the same modeling and analysis capabilities in a Python environment. Unlike the Tcl version, both **sequential and parallel capabilities** are contained **within the single OpenSeesPy package**.

Because Python scripts are interpreted, when running OpenSeesPy in parallel, **MPI spawns multiple independent Python interpreters**, each of which loads the OpenSeesPy library and executes the Python script:
```
mpiexec -np 4 python model.py
```

In this case:
- MPI launches 4 separate Python processes.
- Each process imports and uses OpenSeesPy independently.
- The script itself must be written with parallel behavior in mind (e.g., using mpi4py, or OpenSeesPy’s support for OpenSeesMP-style decomposition).

It's important to note that the parallel capabilities of Tcl-based OpenSees—OpenSeesSP and OpenSeesMP—have been consolidated into the OpenSeesPy library. So when using OpenSeesPy, you're accessing the same underlying parallel solvers, just through Python. However, OpenSeesPy may not support automatic domain decomposition -- OpenSeesSP.
There are different methods to run OpenSeesPy for parallel, make sure you select the one that meets your needs without significant overhead, not limitations. For example, concurrent.futures may not work using two different nodes.


| Method               | Description                                 |
| -------------------- | ------------------------------------------- |
| Built-in MPI         | Uses OpenSeesPy’s compiled parallel backend |
| *mpi4py*             | Manual MPI communication via Python         |
| *concurrent.futures* | Independent, embarrassingly parallel jobs   |

* **Built-in MPI**:

    ```bash
    mpiexec -np 4 python model.py
    ```
    
    Inside:
    
    ```python
    import openseespy.opensees as ops
    ops.start()
    print("Process:", ops.getPID(), "/", ops.getNP())
    ```

* **Using mpi4py**:

    ```python
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    ```

* **Using concurrent.futures**:

    ```python
    from concurrent.futures import ProcessPoolExecutor
    import os
    
    def run_sim(i):
        os.system(f"python model.py {i}")
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(run_sim, range(4))
    ```
:::

## Comparison: Tcl-Based OpenSees vs OpenSeesPy (Python)

| Feature                | Tcl-Based OpenSees                             | OpenSeesPy (Python)                             |
|------------------------|------------------------------------------------|--------------------------------------------------|
| Executable Type        | Pre-compiled binaries (*OpenSees*, *OpenSeesSP*, *OpenSeesMP*) | Python script using the OpenSeesPy library       |
| MPI Invocation         | *mpiexec -np N OpenSeesMP model.tcl*          | *mpiexec -np N python model.py*                 |
| Parallel Capabilities  | Parallel via *OpenSeesSP* and *OpenSeesMP*    | Uses same parallel backend via OpenSeesPy       |
| Process Model          | Each MPI process runs the compiled binary     | Each MPI process runs a separate Python interpreter |
| Communication          | Managed via MPI                               | Managed via MPI (internal or via *mpi4py*)      |
| Library Integration    | Separate binaries for SP and MP               | Unified into a single library (OpenSeesPy)      |


```{admonition} Key Notes

- *mpiexec* is required to launch parallel versions for both Tcl and Python.
- OpenSeesMP/OpenSeesSP are separate executables in the Tcl world.
- OpenSeesPy contains both sequential and MPI-based parallel logic in one package.
- Built-in OpenSeesPy MPI support is more reliable in terminal or HPC batch jobs than in Jupyter.
```
