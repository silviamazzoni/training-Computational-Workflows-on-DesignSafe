# Interactive Notebooks

***Interactive Development for your Workflow + Seamless HPC Scaling  on DesignSafe***

Jupyter Notebooks offer an **interactive, visual, and self-documenting workflow**, making them one of the most versatile ways to develop with OpenSees on DesignSafe. They allow you to combine **code, documentation, plots, and results** in a single file that can be shared, rerun, and extended.

---

## Why Use Jupyter Notebooks?

Best suited for users working with:

* *matplotlib* or *plotly* for visualization
* *pandas*, *numpy*, and *scipy* for numerical tasks
* Integrated workflows that need pre-processing, execution, and post-processing in one place

Ideal for:

* Educational content and tutorials
* Reports and documentation
* Rapid prototyping and validation of models

---

## Interactive Mode (Single Node)

When you run commands cell by cell in a notebook, you are in **Interactive Mode**.

* Limited to the resources of your JupyterHub container (**single node, up to 8 cores and 20 GB RAM**).
* Great for experimentation, debugging, and incremental model building.
* Not suitable for large, parallel, or multi-node jobs.
* For example, you can run OpenSees interactively using the OpenSeesPy module.

This is conceptually the same as typing commands into a Python console, except you get the added benefit of mixing in plots, markdown explanations, and outputs in one document.

---

## Non-Interactive Mode (Script Execution)

From a notebook, you can also execute **scripts** within shell commands.

* Running a script this way is **non-interactive**: the program starts, reads the script top to bottom, then exits.
* Even in Jupyter, if you run a full script, you’re in non-interactive mode.
* This is the most common way to launch analyses — especially for batch jobs or large models.
* For example, this works for **both Tcl (*OpenSees*) and Python (*python*) versions** of OpenSees.

Examples:

```bash
!OpenSees model.tcl arg1 arg2
```

```bash
!python model.py arg1 arg2
```

⚠️ Note: In this mode, variables defined inside the script do **not** persist in your notebook’s Python kernel, since they run in a separate process.

---

## Caveats of Notebooks

While powerful, notebooks do come with some quirks:

* **Kernel state inconsistencies** — variables may persist unexpectedly between cells, leading to confusion.
* **Out-of-order execution** — running cells out of sequence can produce misleading results.
* **Migration issues** — notebooks often require cleanup when moving workflows to batch jobs.
* **Single-node only** — interactive execution is limited to one container; you must use Tapis to scale.

---

## Scaling Up with Tapis (HPC Mode)

The **recommended way** to move from prototyping to production is to submit jobs directly from a notebook to **TACC HPC systems** using **Tapis** (the Python-accessible API).

* Makes your workflow **seamlessly scalable** — prototype interactively, then submit to HPC without leaving the notebook.
* Supports multi-node parallel jobs (OpenSeesMP, OpenSeesPy + MPI).
* Lets you monitor, retrieve, and post-process results from the same notebook environment.

---

## Quick Comparison

| **Workflow Style**           | **Interactive in Notebook**   | **Script Execution in Notebook**         | **Notebook + Tapis (HPC)**              |
| ---------------------------- | ----------------------------- | ---------------------------------------- | --------------------------------------- |
| **Execution Mode**           | Interactive (cell by cell)    | Non-interactive (script runs then exits) | Batch jobs on HPC                       |
| **Persistence of Variables** | ✅ Variables persist in kernel | ❌ Variables lost (separate process)      | ❌ Variables lost (separate job)         |
| **Parallel/Multi-Node**      | ❌ No (single node only)       | ❌ No (single node only)                  | ✅ Yes (multi-node, MPI)                 |
| **Best For**                 | Learning, debugging, plotting | Full analysis scripts, small jobs        | Large production runs, parameter sweeps |
| **Scalability**              | Limited (8 cores, 20 GB RAM)  | Limited (container resources)            | Scales to thousands of cores            |

Perfect — here’s a **Recommended Practices** subsection you can drop at the end of your Jupyter Notebook section. It ties back to your CLI and console material while giving readers a clear workflow strategy:

---

### Recommended Practices

* **Start Interactive in Jupyter**
  Use Jupyter notebooks with **OpenSeesPy interactively** (cell-by-cell) when learning, debugging, or building small models. The combination of code, plots, and documentation makes it the best environment for exploration.

* **Test with Scripts Inside the Notebook**
  Once a model grows, run Tcl or Python scripts in **non-interactive mode** from your notebook using shell calls. This mimics how your job will behave in production, but keeps testing convenient.

* **Transition to Tapis for Scale**
  When ready for larger workloads, submit jobs to **HPC via Tapis** directly from the notebook. This ensures:

  * Reliable execution on multi-core and multi-node systems
  * No kernel state issues
  * A seamless path from prototype to production

* **Keep Scripts Modular**
  Write your models in clean, reusable Tcl or Python files. In notebooks, focus on orchestration, visualization, and workflow control rather than putting the entire model inline.

* **Document Your Workflow**
  Treat notebooks as living lab books — record assumptions, parameters, plots, and results. This is invaluable for sharing with collaborators or revisiting analyses later.

---

👉 Notebooks are not not a replacement for scripts or HPC, they are the **hub** where development, documentation, and scaling all come together.
