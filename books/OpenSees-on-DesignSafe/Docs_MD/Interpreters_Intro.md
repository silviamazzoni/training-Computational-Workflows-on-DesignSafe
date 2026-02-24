# OpenSees-Tcl & OpenSeesPy
***OpenSees Interpreters***

There are two main interpreter-based versions of **OpenSees**:

* **OpenSees-Tcl**, which uses the Tcl scripting language and is distributed as standalone executables.
* **OpenSeesPy**, which is a Python library that extends Python with OpenSees-specific commands.

At the core, both are compiled from the same source code and perform the same types of structural and geotechnical simulations. The difference lies in **how they’re executed**, which impacts your workflow on HPC systems, in Jupyter, and when designing automated pipelines.

:::{admonition} **Quick Comparison**
**OpenSees-Tcl** runs as an external executable—great for stable batch scripts and domain-decomposed **OpenSeesSP** jobs—while **OpenSeesPy** runs *inside Python*, letting you interrogate and steer the model during execution, integrate with scientific Python, and smoothly scale via **Tapis** to large parametric studies (with **OpenSeesMP** or *mpi4py*). Use **OpenSees-Express** for quick sequential jobs and first-time runs; move to Jupyter for interactive development; and submit production jobs with Tapis for automation, provenance, and scale.
:::

## How they run

:::{dropdown} **OpenSees-Tcl**

This version is a **self-contained executable application** that bundles the Tcl interpreter. You run it by calling an OpenSees command at the terminal or in a job script, typically providing your input file as a command-line argument. For example:

```bash
OpenSees model.tcl
```

When no input file is given, **OpenSees** runs in **interactive mode**, prompting you for commands one at a time. When an input file is given right after the command, internally, OpenSees “sources” your Tcl script — meaning it reads and executes each command inside the file using its embedded Tcl interpreter.

Executables like `OpenSees`, `OpenSeesMP`, and `OpenSeesSP` are separate binaries. You choose the one that fits your analysis (sequential, parallel with shared memory, or parallel with distributed memory).

:::

:::{dropdown} **OpenSeesPy**

This version is a **Python library**, not a standalone executable. You run OpenSeesPy by invoking Python, which then loads your script that imports the OpenSeesPy module:

```python
import openseespy.opensees as ops
```

So instead of calling a specialized OpenSees program, you run:

```bash
python model.py
```

where `model.py` is a standard Python script that builds your model and analysis using OpenSeesPy’s functions. When no input file is given, **python** runs in **interactive mode**, prompting you for commands one at a time.


Because OpenSeesPy sits inside Python, it benefits from Python’s full ecosystem for data processing, visualization, and automation. However, support for `OpenSeesMP` and `OpenSeesSP` features in OpenSeesPy can vary by platform, so it’s recommended to test parallel capabilities explicitly on Jupyter Hub vs the HPC environment.

:::

This setup — where an application either wraps its own interpreter (like OpenSees-Tcl) or extends an existing one (like OpenSeesPy) — is **standard in computational research**. Most HPC applications work this way:

* You run a command at the CLI, optionally pass an input file, and the program processes commands line by line.
* This direct use of the **command-line interface (CLI)** is essential on HPC systems. It gives you complete control, enables robust automation, and allows scaling analyses across thousands of cores or parameter sets, all without relying on graphical interfaces.
* And in truth, **almost all programs are run this way under the hood** — whether you type the command in a terminal, click a "Run" button in a GUI, or submit a job through a web portal, it ultimately launches a process that runs the same core command-line invocation.

## Summary comparison

| **Aspect**               | **OpenSees-Tcl**                                             | **OpenSeesPy**                                             |
| ------------------------ | ------------------------------------------------------------ | ---------------------------------------------------------- |
| **Interpreter Language** | Tcl                                                          | Python                                                     |
| **Execution Method**     | Run via OpenSees executable (`OpenSees`, `OpenSeesMP`, etc.) | Run Python script with `import openseespy.opensees as ops` |
| **File Type**            | `.tcl` script                                                | `.py` script                                               |
| **Input File Handling**  | Passed as command-line argument; sourced internally          | Python runs the script; functions call OpenSeesPy commands |
| **Executable Variants**  | Separate binaries: OpenSees, OpenSeesMP, OpenSeesSP          | Typically a single package; may or may not support MP/SP   |
| **Interactive Mode**     | Available when run with no arguments                         | Available when Python run with no script                   |
| **Source Code**          | Same for both versions                                       | Same for both versions                                     |
| **Usage Style**          | Terminal/CLI call to executable                              | Run Python script through Python interpreter               |
| **Import Required?**     | No                                                           | Yes (`import openseespy.opensees as ops`)                  |
| **Recommended For**      | Legacy scripts, direct CLI usage                             | Python workflows, scripting integration, data handling     |
