# Parameter Sweeps
***Using job arrays for powerful automated parameter sweeps***

## EXAMPLE: a small SLURM job array for parameter sweeps

A **SLURM job array** is a powerful way to run many similar jobs (e.g. varying a parameter or input file) without submitting hundreds of individual `sbatch` commands.

* Here’s a simple template that runs `OpenSees` on different input files named `model_1.tcl`, `model_2.tcl`, ..., `model_10.tcl`:

    ```bash
    #!/bin/bash
    #SBATCH -J ParamSweep
    #SBATCH -o output.%A_%a.out
    #SBATCH -e output.%A_%a.err
    #SBATCH -p normal
    #SBATCH -N 1
    #SBATCH -n 4
    #SBATCH -t 00:30:00
    #SBATCH --array=1-10
    
    module load intel
    module load OpenSees/3.3.0
    
    cd $SCRATCH/my_sweep_project
    
    # Run the OpenSees model for this index
    OpenSees model_${SLURM_ARRAY_TASK_ID}.tcl
    ```

**How it works**

* `--array=1-10` tells SLURM to run this script **10 times**, with `SLURM_ARRAY_TASK_ID` taking values from `1` to `10`.
* The `%A` in the output filename is replaced by the **main SLURM job ID**, and `%a` is replaced by the **array index**, so you get outputs like:

  ```
  output.1234567_1.out
  output.1234567_2.out
  ...
  output.1234567_10.out
  ```
* Inside the script, `${SLURM_ARRAY_TASK_ID}` picks the right input file.


This is a classic way to do parameter sweeps or ensemble runs without manually submitting multiple jobs — it’s **more scheduler-friendly** and makes monitoring easier.




## EXAMPLE: SLURM job array for Python scripts with parameters

Imagine you have a single Python script, `run_analysis.py`, which takes a numeric parameter from the command line, like:

```bash
python run_analysis.py 10
```

to set, say, the load magnitude, number of stories, or other analysis variable.

You can run a sweep of 10 different values with a job array.

## Example SLURM script: `job_array_python.slurm`

```bash
#!/bin/bash
#SBATCH -J ParamSweepPy
#SBATCH -o output.%A_%a.out
#SBATCH -e output.%A_%a.err
#SBATCH -p normal
#SBATCH -N 1
#SBATCH -n 4
#SBATCH -t 00:15:00
#SBATCH --array=1-10

module load python3

cd $SCRATCH/my_python_project

# Pass SLURM_ARRAY_TASK_ID as a command-line argument to your script
python run_analysis.py ${SLURM_ARRAY_TASK_ID}
```



* **What’s happening here?**

    * `--array=1-10` runs this script 10 times, with `${SLURM_ARRAY_TASK_ID}` taking values from `1` to `10`.
    * Your Python script reads that value from `sys.argv`:
    
    ```python
    import sys
    
    param = int(sys.argv[1])
    print(f"Running analysis with parameter: {param}")
    
    # rest of your OpenSeesPy model setup using `param`
    ```
    
    * Each run gets its own output file:
    
      ```
      output.1234567_1.out
      output.1234567_2.out
      ...
      output.1234567_10.out
      ```
    
    
    This pattern is incredibly flexible. You can:
    
    * Map array IDs to a lookup file with different parameter sets.
    * Use `SLURM_ARRAY_TASK_ID` to select different input files or load different config lines.
    


## EXAMPLE: driving job arrays from a CSV of parameters

This is a **short, super-practical example** of using a **lookup file** (CSV or text) to drive your parameter sweeps via `SLURM_ARRAY_TASK_ID`. This is very common in large ensembles or multi-variable studies.

* **Your parameter file**

    Make a simple text or CSV file, e.g. `params.csv`:
    
    ```
    10
    20
    30
    40
    50
    60
    70
    80
    90
    100
    ```
    
    Each line is a parameter you want to use.

* **Your Python script**

    Your `run_analysis.py` reads which line to use based on the array task ID:
    
    ```python
    import sys
    
    # This script assumes SLURM_ARRAY_TASK_ID passed as sys.argv[1]
    task_id = int(sys.argv[1])
    
    # Read the correct line from the parameter file
    with open("params.csv") as f:
        lines = f.readlines()
        param = int(lines[task_id - 1].strip())  # SLURM_ARRAY_TASK_ID is 1-based
    
    print(f"Running analysis with parameter: {param}")
    
    # Here you could set up your OpenSeesPy model or whatever you want
    # ops.load(nodeTag, *loads) or similar
    ```
    
    **Note:** The `task_id - 1` is because SLURM array IDs start at 1, but Python lists start at 0.

* **Your SLURM script**

    ```bash
    #!/bin/bash
    #SBATCH -J ParamSweepCSV
    #SBATCH -o output.%A_%a.out
    #SBATCH -e output.%A_%a.err
    #SBATCH -p normal
    #SBATCH -N 1
    #SBATCH -n 4
    #SBATCH -t 00:20:00
    #SBATCH --array=1-10
    
    module load python3
    
    cd $SCRATCH/my_python_project
    
    # Copy the params file to scratch if needed
    cp ~/my_local_dir/params.csv .
    
    python run_analysis.py ${SLURM_ARRAY_TASK_ID}
    ```

* **Why this is powerful**

    * You can drive **complex studies with many input values** from a single CSV or text file.
    * Each job in the array automatically reads its assigned parameter and runs independently.
    * This is the HPC-friendly way to do **large parameter sweeps, sensitivity analyses, or Monte Carlo simulations**.


## EXAMPLE: multiple parameters from a CSV row

Here is an extension of the same idea, but now reading **multiple parameters per job from a CSV row**, so you can vary several model inputs at once (like *load, height, damping*)

* **Your CSV parameter file**

    Let’s say you have a file called `params.csv` that looks like this:
    
    ```
    load,height,damping
    10,5,0.02
    20,10,0.03
    30,15,0.04
    40,20,0.05
    50,25,0.06
    ```


* **Your Python script**
    
    Now `run_analysis.py` reads the correct line based on `SLURM_ARRAY_TASK_ID`:
    
    ```python
    import sys
    
    task_id = int(sys.argv[1])
    
    with open("params.csv") as f:
        lines = f.readlines()
        if task_id == 1:
            header = lines[0]  # skip header
        line = lines[task_id]  # line indexing is offset by 1 due to header
    
    # Split line into parameters
    load, height, damping = line.strip().split(',')
    
    # Convert to appropriate types
    load = float(load)
    height = float(height)
    damping = float(damping)
    
    print(f"Running analysis with load={load}, height={height}, damping={damping}")
    
    # Use these variables to set up your model, e.g.
    # ops.load(..., load)
    # ops.node(..., height)
    # ops.rayleigh(..., damping, ...)
    ```

    **Note:**
            
            * `task_id == 1` corresponds to the header line in most CSVs, so data starts at `task_id == 2`.
            * This is a common pitfall — watch your indexing if you have a header row!

* **Your SLURM job array script**

    ```bash
    #!/bin/bash
    #SBATCH -J MultiParamSweep
    #SBATCH -o output.%A_%a.out
    #SBATCH -e output.%A_%a.err
    #SBATCH -p normal
    #SBATCH -N 1
    #SBATCH -n 4
    #SBATCH -t 00:20:00
    #SBATCH --array=2-6  # start at 2 to skip header line
    
    module load python3
    
    cd $SCRATCH/my_python_project
    cp ~/my_local_dir/params.csv .
    
    python run_analysis.py ${SLURM_ARRAY_TASK_ID}
    ```

## Summary: super scalable studies

| What changes across runs?          | How?                            |
| ---------------------------------- | ------------------------------- |
| Load, height, damping coefficients | Controlled by `params.csv`      |
| Which line each job uses           | Driven by `SLURM_ARRAY_TASK_ID` |

This lets you easily launch **dozens, hundreds, or thousands of varied analyses** with a single job submission, each automatically pulling its unique inputs.


