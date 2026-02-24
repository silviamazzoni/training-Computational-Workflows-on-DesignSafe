# Command-Line Arguments
***Flexible, Reusable, and Automatable Simulations***
***Optional***

OpenSees (both Tcl and Python) supports passing command-line arguments, allowing you to control your simulation behavior at runtime without editing the script itself. This is essential for parameter studies, calibration runs, job arrays, and high-throughput automation.

## Why Use Command-Line Arguments?

* Avoid duplicating scripts for each input variation
* Customize simulations dynamically at runtime
* Enable parameter sweeps, job arrays, and automation
* Keep job inputs visible in logs and reproducible
* Simplify integration with Tapis, Slurm, or bash scripts


## Use Cases

| Use Case                     | Benefit                                                   |
| ---------------------------- | --------------------------------------------------------- |
| Parameter studies            | Vary geometry, loads, or materials across runs            |
| Job arrays on Slurm or Tapis | Pass different arguments to identical jobs                |
| Model calibration or UQ      | Use command-line control for thousands of simulation runs |
| Organizing output            | Pass output folder names from the command line            |


## How to Pass Arguments

You append arguments after the script name:


**Tcl:**

```bash
OpenSees model.tcl 2 output_folder/
```


**Python (OpenSeesPy):**

```bash
python model.py 2 output_folder/
```

**Parallel Execution:**

```bash
mpiexec -np N OpenSeesMP modelMP.tcl 2 output_folder/
mpiexec -np N python model.py 2 output_folder/
```

## How to Read Arguments Inside the Script

:::{dropdown} Tcl (OpenSees, OpenSeesMP, OpenSeesSP)
    
Tcl automatically provides:

* `argv` — List of command-line arguments
* `argc` — Number of arguments

**Example – model.tcl**

```tcl
set argc [llength $argv]
set modelType [lindex $argv 0]
set outputDir [lindex $argv 1]

puts "Running model type: $modelType"
puts "Saving results to: $outputDir"
file mkdir $outputDir
```
:::

::::{dropdown} Python (OpenSeesPy)

Use the *sys* module to access:

* `sys.argv[0]` → Script name
* `sys.argv[1:]` → Arguments

**Example – model.py**

```python
import sys
import os
import openseespy.opensees as ops

model_type = int(sys.argv[1])
output_dir = sys.argv[2]

print(f"Running model type: {model_type}")
print(f"Saving results to: {output_dir}")
os.makedirs(output_dir, exist_ok=True)

if model_type == 1:
    # Define Model 1
    pass
elif model_type == 2:
    # Define Model 2
    pass
```


:::{dropdown} Using *argparse* in Python (Recommended)

For more robust input handling, use the *argparse* module:

**Run:**

```bash
python model.py --model 2 --output output_folder/
```

**Script:**

```python
import argparse
import os
import openseespy.opensees as ops

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=int, required=True)
parser.add_argument("--output", type=str, default="output")
args = parser.parse_args()

print(f"Model: {args.model}, Output Dir: {args.output}")
os.makedirs(args.output, exist_ok=True)

if args.model == 1:
    # Define Model 1
    pass
elif args.model == 2:
    # Define Model 2
    pass
```
:::

::::
## Automating Parameter Sweeps

You can control OpenSees (**Tcl or python**) runs from another Python script (or Jupyter Notebook cell):

**Python controller script:**

```python
import os

model_types = [1, 2, 3]
for m in model_types:
    out_dir = f"results/model_{m}"
    os.system(f"OpenSees model.tcl {m} {out_dir}")
    os.system(f"python model.py --model {m} --output {out_dir}")
```

```{admonition} Tip: Use This in Jupyter!
You can run the controller above inside a Jupyter notebook cell to launch multiple simulations interactively.

Great for:
- Parameter studies
- Monte Carlo simulations
- Generating data for plots
```


## Summary Table

| Language | Access Pattern              | Example                      |
| -------- | --------------------------- | ---------------------------- |
| Tcl      | **$argv**, **[lindex $argv N]** | **[lindex $argv 0]**           |
| Python   | **sys.argv[N]` or **argparse** | **sys.argv[1]**, **args.output** |

