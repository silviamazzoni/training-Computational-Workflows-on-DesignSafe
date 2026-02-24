# Workflow in JupyterHub
***Analysis Workflow within JupyterHub***
  
You can use the jupyter environment to supports your entire workflow, or just parts of it:
1. **Edit** your input scripts in the text editor, and test them in real-time as you build your model and analyses.
2. **Run** OpenSees analyses
    - Run your small jobs directly within Jupyter
       * Run OpenSees, OpenSeesMP, or OpenSeesSP at the terminal (or from a jupyter notebook)
       * Run Python with your OpenSeesPy script at the terminal (or from a jupyter notebook)
       * Run OpenSeesPy integrated into a Jupyter Notebook
    - Submit your larger jobs to the HPC system
       * Submit your OpenSees-TCL scripts via the the DesignSafe Web Portal
       * Submit your OpenSees-TCL or OpenSeesPy script via Tapis in a Jupyter Notebook
       * Create a SLURM-JOB file, SSH into the HPC system and submit your SLURM job (OpenSees-TCL or OpenSeesPy)
3. **Post-process** your analyses using Python, Jupyter Notebooks, Matlab, etc.
