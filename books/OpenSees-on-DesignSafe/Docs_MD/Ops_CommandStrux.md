# Command Structure
***Command Structure & Execution Modes***

OpenSees (and OpenSeesPy via Python) is a **command-driven application** designed to run simulations by executing a series of modeling and analysis instructions. How you invoke OpenSees directly determines the mode of execution, and understanding this distinction is crucial for effective and scalable use of the software.

This section introduces the three primary execution modes and the structure of typical OpenSees commands. These concepts are foundational and apply regardless of the interface you're using—whether on a local machine, an HPC cluster, or inside DesignSafe's Jupyter environment. 

At a high level, an application command (whether Tcl or Python) has **three key components**:

1. **Executable File** – Specifies the program to run
2. **Input Script** *(optional)* – File containing modeling and analysis commands
3. **Command-Line Arguments** *(optional)* – External values passed into the script

These components correspond to three primary **execution modes**, which refer to to **how you run a simulation.** This affects everything from how variables are set to how results are saved.

* **Interactive Mode** – Enter commands one at a time. Each command is executed once entered.
* **Non-Interactive Mode** – Execute a full script from top to bottom
* **Advanced Non-Interactive Mode** – Run a script with external input variables

Each mode plays an important role in OpenSees workflows, from quick tests to full HPC-scale parameter studies.


## Execution Modes

| Mode                         | How to Invoke                                              | When to Use                                 |
| ---------------------------- | ---------------------------------------------------------- | ------------------------------------------- |
| **Interactive**              | Just run the executable (e.g., *OpenSees* or *python*)     | For quick tests, model inspection, learning |
| **Non-Interactive**          | Add input file (e.g., *OpenSees model.tcl*)                | For full analyses or reproducible scripts   |
| **Advanced Non-Interactive** | Add command-line args (e.g., *OpenSees model.tcl 1.0 2.0*) | For automation, sweeps, HPC workflows       |



### Why This Matters

Each execution style supports a different stage of the modeling process:

* Interactive mode is great for **trial-and-error and exploration**.
* Non-interactive mode is essential for **repeatable workflows**.
* Advanced argument passing enables **automation and scalability**.

Understanding and switching between these modes is key to moving from small, test cases to full-scale HPC simulations.

