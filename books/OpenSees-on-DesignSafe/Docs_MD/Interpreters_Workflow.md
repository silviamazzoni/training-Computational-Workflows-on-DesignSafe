# Interpreter Worflows
***OpenSees-Tcl vs OpenSeesPy: Workflow Patterns & App Selection***

## Conceptual difference (why workflows feel different)

* **OpenSees-Tcl** is a standalone executable. You launch it as its own process; control and visibility live *inside* that process. External tools can’t easily “peek” while it runs except via files/logs you write.
* **OpenSeesPy** runs *inside Python*. Python is the main runtime; OpenSees is a library you call. Your script can inspect/modify state mid-analysis, branch logic based on results, stream metrics to dashboards, and coordinate other Python tools (NumPy, pandas, Plotly, mpi4py, etc.).

**Implication:** with OpenSeesPy your workflow code can *query and steer* the model during an analysis; with OpenSees-Tcl you typically coordinate via input files, checkpoints, and post-processing.

---

## Common workflow patterns

### Interactive development (iterate, visualize, debug)

* **Best with:** OpenSeesPy in a Jupyter Notebook (single thread).
* **Why:** Tight feedback loop, inline plots/tables, easy parameter sweeps at small scale.
* **Tip:** When it’s “right,” graduate the same Python code to batch runs via Tapis.

### Batch runs at scale (automate, reproduce, share)

* **Best with:** Python scripts (OpenSeesPy) or Tcl scripts, submitted via **Tapis** (Web Portal or Python SDK).
* **Why:** Job metadata, inputs/outputs, and logs are tracked; trivial to rerun or parameterize.

### Parallelism style

* **Embarrassingly parallel sweeps** (many independent runs):
  Use **OpenSeesMP** or Python + **mpi4py**/**concurrent.futures**; map one case per rank/worker.
* **Single large model that needs distributed memory / domain decomposition**:
  Use **OpenSeesSP**.

### Tight coupling with other Python tools (ML, filtering, live metrics)

* **Best with:** OpenSeesPy (inside Python).
  Stream intermediate results, adapt time-steps, trigger early stop, etc.

---

## Which app is best for which use case?

| Use case                                                 | Recommended app / environment                              | Why it’s a good fit                                 | Notes / trade-offs                                             |
| -------------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------- | -------------------------------------------------------------- |
| Quick, small **sequential** runs; “first job” experience | **OpenSees-Express (sequential VM)** via Web Portal        | No queue, minimal inputs, fast turnaround           | Shared VM, no GUI; great for correctness checks & small models |
| Interactive prototyping, plotting, teaching              | **JupyterHub + OpenSeesPy**                                | Single-threaded, rich notebooks, inline plots       | Not for big parallel jobs; scale later via Tapis               |
| Many independent analyses (records/parameters)           | **OpenSeesMP** (Web Portal / Tapis) or **Python + mpi4py** | One case per rank; high throughput                  | Ensure per-case I/O is isolated; use scratch/work storage      |
| One very large model (memory/DOF heavy)                  | **OpenSeesSP** (Web Portal / Tapis)                        | Domain decomposition across ranks                   | Requires parallel solvers; expect longer queue times           |
| Python-centric pipelines (pre/post + control during run) | **OpenSeesPy + Tapis** (programmatic)                      | Full Python ecosystem; easy automation & provenance | Use *mpi4py* or job arrays to scale                            |
| Legacy Tcl scripts, reproducible batch                   | **OpenSees (Tcl) via Web Portal/Tapis**                    | Stable scripts; minimal refactor                    | Coordination & mid-run queries via files/logs                  |

---

## Decision guide (quick chooser)

1. **Need to poke the model mid-run or use Python tooling?** → **OpenSeesPy**.
2. **Independent sweeps?** → **OpenSeesMP** (or Python + *mpi4py*).
3. **One huge model that must distribute DOFs/memory?** → **OpenSeesSP**.
4. **Just testing sequential logic or teaching?** → **Notebook (OpenSeesPy)** or **OpenSees-Express**.
5. **Ready to scale or automate?** → Submit via **Tapis** (Web Portal or Python SDK).

---

## Example workflows

### A. Notebook → Batch at scale (OpenSeesPy)

1. Prototype in Jupyter (plots, sanity checks).
2. Move the notebook logic into a *model.py* script.
3. Use **Tapis** to submit many runs (vary IM levels, records, parameters).

   * For MPI: *ibrun python -m mpi4py model.py --cases cases.json*
   * For arrays: job array or many small jobs.

### B. Legacy Tcl → Parallel domain model (OpenSeesSP)

1. Validate sequential Tcl on small DOFs.
2. Migrate to SP (domain decomposition objects).
3. Submit via **Tapis**; monitor *.out*/*.err*, extract results to structured files for post-processing.

### C. Embarrassingly parallel sweeps (OpenSeesMP)

1. Design a single Tcl/Py driver that reads one case spec.
2. Launch **OpenSeesMP** and assign one spec per rank.
3. Aggregate outputs (each rank writes to a unique subfolder).

---

## Practical tips & pitfalls

* **Notebook limits:** single process; great for learning and viz, not for production parallel runs.
* **Storage layout:** keep one output folder per run/rank to avoid collisions; prefer work/scratch storage for performance.
* **Logging:** always check SLURM **.out*/**.err* first; stream key metrics to a lightweight CSV for quick triage.
* **Reproducibility:** pin versions (modules/containers), record seeds/IMs/parameters in metadata, archive outputs consistently.
* **Graduation path:** prototype (Notebook) → script (CLI) → scale (Tapis) with **no logic rewrites**, only a change in launcher/parameters.
