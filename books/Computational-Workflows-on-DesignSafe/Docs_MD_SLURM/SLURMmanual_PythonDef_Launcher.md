# Python Launcher def
***Python helper to create a launcher-based sweep (single job)***

Below is a pattern for a **single SLURM job** that uses a **launcher** (parametric/throughput inside one allocation) instead of a **job array**. The idea is the same:

* Read your CSV
* Create a *task list* (one command per row)
* Run that task list with a launcher (e.g., **PyLauncher** at TACC, or a simple GNU `parallel` fallback)
* Still emit a **README_jobs.txt** audit trail

This writes:

1. A SLURM script **without `--array`**
2. A `commands_<job>.txt` file (one command per CSV row)
3. A `README_jobs_<job>.txt` summary

```python
from pathlib import Path

def create_slurm_launcher_sweep(
    csv_file,
    job_name="ParamSweep",
    output_prefix="output",
    nodes=1,
    tasks_per_node=48,           # cores per node you want to use (or "slots")
    time="00:20:00",
    partition="normal",
    workdir="$SCRATCH/my_project",
    # command template: use {row} (1-based data row index), {i} (0-based), {line} (raw csv line), {fields} (list)
    run_cmd_template="python run_analysis.py --row {row}",
    launcher="pylauncher",       # "pylauncher" or "parallel"
    max_concurrent=None          # cap concurrent tasks (defaults to total slots)
):
    """
    Creates a single SLURM script that runs many parameter cases inside one allocation
    using a launcher (PyLauncher or GNU parallel), plus a commands file and README summary.

    CSV is assumed to have a header in row 1.
    Data rows are numbered starting at 2 (matching your prior array convention).
    """
    csv_path = Path(csv_file)
    base = job_name

    # Read CSV lines
    lines = csv_path.read_text().splitlines()
    if len(lines) < 2:
        raise ValueError(f"{csv_file} has no data rows.")

    header = lines[0].strip()
    data_lines = [ln.strip() for ln in lines[1:] if ln.strip()]
    num_jobs = len(data_lines)

    # Build commands file content (one command per CSV data row)
    cmds = []
    for i, line in enumerate(data_lines):
        row = i + 2  # keep same convention: header=1, first data row=2
        fields = [f.strip() for f in line.split(",")]
        cmd = run_cmd_template.format(row=row, i=i, line=line, fields=fields)
        cmds.append(cmd)

    commands_filename = f"commands_{base}.txt"
    Path(commands_filename).write_text("\n".join(cmds) + "\n")

    # README audit trail
    readme_name = f"README_jobs_{base}.txt"
    with open(readme_name, "w") as f:
        f.write(f"Launcher parameter sweep generated for {job_name}\n\n")
        f.write(f"CSV file: {csv_file}\n")
        f.write(f"CSV header: {header}\n")
        f.write(f"Number of jobs: {num_jobs}\n")
        f.write(f"Row numbering: first data row = 2 (header = 1)\n\n")
        f.write("Job details:\n")
        for i, line in enumerate(data_lines, start=2):
            f.write(f"  Row {i}: {line}\n")

    total_slots = nodes * tasks_per_node
    if max_concurrent is None:
        max_concurrent = total_slots

    # Build SLURM script
    slurm_filename = f"{base}.slurm"
    script = f"""#!/bin/bash
#SBATCH -J {job_name}
#SBATCH -o {output_prefix}.%j.out
#SBATCH -e {output_prefix}.%j.err
#SBATCH -p {partition}
#SBATCH -N {nodes}
#SBATCH --ntasks-per-node={tasks_per_node}
#SBATCH -t {time}

set -euo pipefail

echo "Job started: $(date)"
echo "Running on nodes: $SLURM_JOB_NUM_NODES"
echo "Working dir: {workdir}"

cd {workdir}

# Stage inputs (adjust as needed)
cp -f {csv_file} . || true
cp -f {commands_filename} .

echo "Total cases: {num_jobs}"
echo "Total slots (nodes * tasks_per_node): {total_slots}"
echo "Max concurrent tasks: {max_concurrent}"

# Load your environment here
# module load python3
# module load opensees
# module load pylauncher   # if needed on your system

"""

    if launcher.lower() == "pylauncher":
        # This is a *template* since PyLauncher setups vary a bit by site/version.
        # The key is: one-line-per-task file + run it within the allocated cores.
        script += f"""
#############################################
# Option A: PyLauncher-style execution
#############################################
# Typical workflow:
#  1) commands file: one command per line (already created)
#  2) run a launcher that dispatches up to {max_concurrent} tasks across allocated cores

# If your site provides a helper like "paramrun" or a pylauncher CLI, call it here.
# Examples you may adapt (site-specific):
#   python -m pylauncher.launcher --commandfile commands_{base}.txt --nprocs {max_concurrent}
#   paramrun commands_{base}.txt

echo "Launching with PyLauncher (site-specific command may need adjustment)"
python - <<'PY'
import os, subprocess, sys

cmdfile = "commands_{base}.txt"
nprocs  = {max_concurrent}

# --- Replace this block with the exact PyLauncher invocation for your system ---
# As a safe default, we fall back to GNU parallel if available; otherwise run serial.
if subprocess.call(["bash","-lc","command -v parallel >/dev/null 2>&1"]) == 0:
    print("Using GNU parallel fallback (parallel detected).")
    sys.exit(subprocess.call(["bash","-lc", f"parallel -j {nprocs} < {cmdfile}"]))
else:
    print("WARNING: PyLauncher not invoked (no site-specific command provided) and GNU parallel not found.")
    print("Running serially.")
    with open(cmdfile) as f:
        for line in f:
            line=line.strip()
            if not line: 
                continue
            ret = subprocess.call(line, shell=True)
            if ret != 0:
                raise SystemExit(ret)
PY

"""
    else:
        # GNU parallel option: widely portable if installed
        script += f"""
#############################################
# Option B: GNU parallel execution
#############################################
# Runs up to {max_concurrent} cases at once within this single allocation.
# Requires: GNU parallel available on the system.
parallel -j {max_concurrent} < commands_{base}.txt

"""

    script += """
echo "Job finished: $(date)"
"""

    Path(slurm_filename).write_text(script)

    print(f"Generated: {slurm_filename}")
    print(f"Generated: {commands_filename}")
    print(f"Generated: {readme_name}")
    print(f"Cases: {num_jobs} (run inside one job using launcher='{launcher}')")
```

---

## How you use it

* **Python sweep (same semantics as your array, but launcher-based)**

```python
create_slurm_launcher_sweep(
    "params.csv",
    job_name="ParamSweep",
    nodes=2,
    tasks_per_node=48,
    run_cmd_template="python run_analysis.py --row {row}",
    launcher="pylauncher",     # or "parallel"
    max_concurrent=96          # often = nodes*tasks_per_node
)
```

* **OpenSees Tcl indexed by row number**

```python
create_slurm_launcher_sweep(
    "params.csv",
    job_name="OpenSeesSweep",
    nodes=1,
    tasks_per_node=48,
    run_cmd_template="OpenSees model_{row}.tcl",
    launcher="parallel"
)
```

* **If your run script reads the CSV line directly**

```python
create_slurm_launcher_sweep(
    "params.csv",
    job_name="LineDrivenSweep",
    run_cmd_template="python run_analysis.py --params '{line}'",
    launcher="parallel"
)
```

---

## What changes vs a job array?

* **No `#SBATCH --array=...`**
* You get a `commands_*.txt` file that replaces the scheduler array index list
* One allocation; launcher fills the cores with independent tasks
* Output/logging is typically per *single job*, so if you want per-case logs, build that into `run_cmd_template`, e.g.
  `python run_analysis.py --row {row} > logs/case_{row}.out 2> logs/case_{row}.err`

