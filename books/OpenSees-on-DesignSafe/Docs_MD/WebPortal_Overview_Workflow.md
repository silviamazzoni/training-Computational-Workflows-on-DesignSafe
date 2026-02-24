# Web-Portal Workflow
***End-to-End Workflow: JupyterHub + Web Portal***

This recommended workflow integrates both the Web Portal and JupyterHub to leverage their strengths:

1. **Create and Test Input File (in JupyterHub)**  
   - Build *.tcl* or *.py* scripts using a notebook or the Jupyter editor  
   - Optionally test small models within JupyterHub (recommended)

2. **Submit Job via Web Portal**  
   - Go to the [DesignSafe Web Portal](https://www.designsafe-ci.org/)
   - Select *OpenSees-Express*, *OpenSeesMP*, or *OpenSeesSP*
   - Choose your working directory (containing all files)
   - Select the main input script (e.g., *model.tcl*)
   - Set compute resources (cores, wall time)
   - Launch the job — Tapis handles the rest  

3. **Retrieve and Visualize Output**  
   - When the job completes, results are returned to **My Data**  
   - Open your Jupyter environment to explore logs, time histories, or other outputs  

4. **Post-Process in Jupyter** *(covered in future modules)*  
   - Use Python scripts or notebooks for advanced visualization and batch post-processing  
   - Automate parameter studies and job submission using the Tapis API (also covered later)


## How It Works Internally

Each Web Portal app is a **Tapis App**, defined using a combination of:

| File           | Purpose                                                                  |
|----------------|--------------------------------------------------------------------------|
| *app.json*     | Defines input fields, main program, and behavior                         |
| *profile.json* | Maps the app to an execution system and loads required modules           |
| *tapisjob_app.sh* | Shell wrapper that builds the OpenSees run command (e.g., with `ibrun`) |
| Container/Image| Defines the compute environment (usually loaded via modules)             |

You can explore these apps in the open-source repository:  
🔗 [WMA-Tapis-Templates on GitHub](https://github.com/TACC/WMA-Tapis-Templates/tree/main/applications)

