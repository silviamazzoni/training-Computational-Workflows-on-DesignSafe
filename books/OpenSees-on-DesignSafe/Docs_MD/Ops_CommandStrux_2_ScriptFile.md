# Input Script File
***Non-Interactive Mode with Script Files (Optional)***

When you run OpenSees or OpenSeesPy with a script file as the first argument, the program will **exit automatically once the script finishes executing**. This is known as **Non-Interactive Mode** — the file is read from top to bottom, and all commands are executed without any additional user input.

This is the **recommended and most common** method for running OpenSees, especially for batch jobs and large analyses.

Even on interactive platforms like **Jupyter**, if you run an entire script in one command, you’re still operating in non-interactive mode.
However, you can combine the convenience of an *input file* with the flexibility of an interactive workflow by loading OpenSeesPy commands directly into notebook cells. This approach lets you develop and refine your models while integrating **graphics, plots, and visualizations** alongside your code.

> **Note:** For large-scale runs on HPC systems, non-interactive mode is the default and most reliable execution style.

---

## Use Cases

  * Full model execution
  * Reproducible simulations
  * Running jobs on HPC or cloud environments
    
## **Sequential Execution**

| Language   | Command                                            |
| ---------- | -------------------------------------------------- |
| Tcl        | *OpenSees inputfile.tcl*                           |
| OpenSeesPy | *python inputfile.py* (*import OpenSeesPy inside inputfile.py*)                          |


    
##  **Parallel Execution (N cores)**

Use **mpiexec**, **mpirun**, or **ibrun** to launch distributed memory jobs:

| Language         | Command                                                                   |
| ---------------- | ------------------------------------------------------------------------- |
| Tcl (MP)         | **mpiexec -np N OpenSeesMP inputfileMP.tcl**                                |
| Tcl (SP)         | **mpiexec -np N OpenSeesSP inputfileSP.tcl**                                |
| OpenSeesPy (MPI) | **mpiexec -np N python inputfile.py** *                                     |

* *(import OpenSeesPy inside. And script must use mpi4py or similar)*
* N is the number of concurrent processors
* Use **mpiexec** in JupyterHub
* Use **ibrun** in the HPC system, such as Stampede3


