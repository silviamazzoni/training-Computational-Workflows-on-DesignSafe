# OpenSees on HPC
***OpenSees on HPC via JupyterHub***

DesignSafe’s JupyterHub provides an interactive environment where you can prepare, submit, and monitor jobs directly on TACC’s HPC systems. Instead of writing your own SLURM scripts, you can use **Tapis Apps**—predefined job templates that take care of loading the correct modules, staging input files, running OpenSees on HPC nodes, and saving results back to your storage.

Running OpenSees this way is especially useful when you want to combine the flexibility of Jupyter notebooks with the power of HPC. You can test or pre-process models interactively, then submit larger production runs to Stampede3 without leaving JupyterHub.

When comparing the available workflows:

* **Web Portal → HPC**
  Easiest to use with a point-and-click interface, but less flexible for automation or scripting.

* **JupyterHub → Local**
  Good for testing small models interactively, but limited to the resources available in JupyterHub (single node).

* **SSH → HPC (manual SLURM)**
  The traditional method: log into Stampede3 via SSH, write your own SLURM job script, and submit with `sbatch`. In addition, you must manually move your input files to the correct **scratch location** before submitting the job, and copy the results back afterward. This provides **maximum control**, but requires more setup and becomes tedious when you need to run many jobs.

  * **Note:** Because Tapis makes this process much more fluid, we will not be covering the SSH method in detail in this training.

* **JupyterHub → HPC via Tapis Apps**
  Combines the best of both worlds: scripting and automation from JupyterHub with the full scalability of HPC. Tapis Apps handle SLURM submission and also take care of staging files in and out of scratch for you, making it especially convenient for large studies or repeated runs.

**Step-by-step workflow (JupyterHub + Tapis Apps):**

1. Prepare your OpenSees input files in your DesignSafe storage — you can do this within JupyterHub.
2. Select the appropriate Tapis App (e.g., OpenSeesMP for parallel jobs).
3. Submit the job from the WebPortal, a Jupyter notebook, or terminal using the app definition.
4. Tapis stages files, launches the job on HPC, and manages the scheduler.
5. Results are returned to your designated storage for post-processing.
6. Postprocess and prepare publication-quality material in JupyterHub.

All of the above steps can be managed from a single Jupyter Notebook.

This approach ensures that you use the same standardized OpenSees applications available through the Web Portal and the Tapis API, keeping your workflows consistent across platforms—while also saving time compared to writing SLURM scripts and manually managing scratch directories.
