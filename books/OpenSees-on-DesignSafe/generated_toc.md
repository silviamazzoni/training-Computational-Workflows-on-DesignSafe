# Table of Contents

## 
- [HOME](HOME.md)
- [Document Objectives](Docs_MD/Objectives.md)
  - [About This Document](Docs_MD/About.md)
  - [Prerequisites](Docs_MD/Prerequisites.md)
  - [Training Material](Docs_MD/TrainingMaterial.md)
- [DocSeries](Docs_MD/DocSeries.md)

## Workflows
- [OpenSees Workflows](Docs_MD/Workflows_OpenSees.md)
- [Job Workflow](Docs_MD/Workflows_Job.md)
- [Training Workflows](Docs_MD/Workflows_Trainings.md)

## OpenSees
- [OpenSees](Docs_MD/OpenSees_AndDesignSafe.md)
- [OpenSees-Tcl & OpenSeesPy](Docs_MD/Interpreters_Intro.md)
  - [Interpreter Worflows](Docs_MD/Interpreters_Workflow.md)
- [Decision Matrix](Docs_MD/Interpreters_DecisionMatrix.md)
- [Command Structure](Docs_MD/Ops_CommandStrux.md)
  - [Executable File](Docs_MD/Ops_CommandStrux_1_ExecutableFile.md)
  - [Input Script File](Docs_MD/Ops_CommandStrux_2_ScriptFile.md)
  - [Command-Line Arguments](Docs_MD/Ops_CommandStrux_3_CommandLineArgs.md)
- [Parallel Execution](Docs_MD/Ops_ParallelExec.md)
  - [Parallel Execution: MPI](Docs_MD/Ops_ParallelExec_MPI.md)
  - [Parallel Execution: ibrun](Docs_MD/Ops_ParallelExec_Ibrun.md)
  - [OpenSeesPy Parallel](Docs_MD/Ops_ParallelExec_python.md)
- [Execution Guide](Docs_MD/Ops_ExecGuide.md)

## Computational Environments
- [Introduction](Docs_MD/ComputeEnvironmentsForOps.md)
- [JupyterHub Environment](Docs_MD/ComputeEnv_JupyterHub.md)
- [Virtual Machines (VMs)](Docs_MD/ComputeEnv_OpenSeesVM.md)
- [HPC on TACC for OpenSees](Docs_MD/ComputeEnv_HPC.md)
- [Compute-Environment Guide](Docs_MD/ComputeEnv_Guide.md)
- [OpenSees on HPC](Docs_MD/RunOpsOnHPC.md)
- [OpenSees from Web Portal](Docs_MD/WebPortal_Overview.md)

## Jupyter Hub
- [OpenSees on JupyterHub](Docs_MD/RunOpsInDS_JupyterHub_intro.md)
- [Terminal CLI](Docs_MD/CLI.md)
  - [Run OpenSees Interactive at the CLI](Docs_MD/RunOpenSees_CLI_interactive.md)
  - [Run OpenSees Script at the CLI](Docs_MD/RunOpenSees_CLI_script.md)
- [Python Console](Docs_MD/RunOpsInDS_Console.md)

## OpenSees Apps
- [DesignSafe Tapis Apps](Docs_MD_Tapis/DSapps_Overview.md)
- [OpenSees Apps on DesignSafe](Docs_MD_Tapis/DSapps_OpenSees.md)
  - [OpenSees Legacy Apps on DesignSafe](Docs_MD_Tapis/DSapps_OpenSees_LegacyApps.md)
  - [DesignSafe Agnostic App on DesignSafe](Docs_MD_Tapis/DSapps_OpenSees_AgnosticApp.md)
- [Inputs for OpenSees Apps](Docs_MD_Tapis/tapis_OpenSeesApps_input.md)
- [The OpenSees Web Portal App](Docs_MD_Tapis/OpenSees_webPortal_app.md)
- [OpenSees-EXPRESS App](Docs_MD_Tapis/OpsApps_Express.md)
  - [App Structure](Docs_MD_Tapis/OpsApps_Express_fileStrux.md)
  - [app.json](Docs_MD_Tapis/OpsApps_Express_app_json.md)
  - [tapisjob_app.sh](Docs_MD_Tapis/OpsApps_Express_app_sh.md)
  - [Example](Docs_MD_Tapis/OpsApps_Express_example.md)
- [OpenSeesMP App](Docs_MD_Tapis/OpsApps_MPs3.md)
  - [App Structure](Docs_MD_Tapis/OpsApps_MPs3_fileStrux.md)
  - [app.json](Docs_MD_Tapis/OpsApps_MPs3_app_json.md)
  - [profile.json](Docs_MD_Tapis/OpsApps_MPs3_profile_json.md)
  - [tapisjob_app.sh](Docs_MD_Tapis/OpsApps_MPs3_tapisjob_app_sh.md)
- [designsafe-openseespy-s3](Docs_MD_Tapis/tapisApp_readme_OpenSeesPy.md)
- [designsafe-agnostic-app](Docs_MD_Tapis/tapisApp_readme_AgnosticApp.md)

## Trainings
- [Web-Portal Workflow](Docs_MD/WebPortal_Overview_Workflow.md)
  - [1 Create Input](Docs_MD/WebPortal_1_CreateInput.md)
  - [2 Submit OpenSees-Express](Docs_MD/WebPortal_2_SubmitJob_OpenSeesExpress.md)
  - [2 Submit OpenSeesMP](Docs_MD/WebPortal_2_SubmitJob_OpenSeesMP.md)
  - [3 Monitor OpenSees-Express](Docs_MD/WebPortal_3_MonitorJob_OpenSeesExpress.md)
  - [3 Monitor OpenSeesMP](Docs_MD/WebPortal_3_MonitorJob_OpenSeesMP.md)
  - [4 PostProcess Ops-Express](Jupyter_Notebooks_OpenSees/webPortal_4_PostProcess_OpenSeesExpress.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_OpenSees/webPortal_4_PostProcess_OpenSeesExpress.ipynb' target='_blank'>Open in JupyterHub</a></sub>
  - [4 PostProcess Ops-MP](Jupyter_Notebooks_OpenSees/webPortal_4_PostProcess_OpenSeesMP.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_OpenSees/webPortal_4_PostProcess_OpenSeesMP.ipynb' target='_blank'>Open in JupyterHub</a></sub>
- [OpenSeesPy in a Notebook](Jupyter_Notebooks_OpenSees/runOps_Ex1a.py.Canti2D.Push.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_OpenSees/runOps_Ex1a.py.Canti2D.Push.ipynb' target='_blank'>Open in JupyterHub</a></sub>
- [ANY OpenSees from a Notebook](Jupyter_Notebooks_OpenSees/runOps_RunAnyOpenSeesInPython.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_OpenSees/runOps_RunAnyOpenSeesInPython.ipynb' target='_blank'>Open in JupyterHub</a></sub>
- [Explore Tapis Apps](Docs_MD_Tapis/tapis_apps_explore.md)
  - [App Schema: opensees-express](Jupyter_Notebooks_TapisAppsOpenSees/tapis_discover_app_OSexpress.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_TapisAppsOpenSees/tapis_discover_app_OSexpress.ipynb' target='_blank'>Open in JupyterHub</a></sub>
  - [App Schema: opensees-mp-s3](Jupyter_Notebooks_TapisAppsOpenSees/tapis_discover_app_OSmpS3.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_TapisAppsOpenSees/tapis_discover_app_OSmpS3.ipynb' target='_blank'>Open in JupyterHub</a></sub>
  - [designsafe-agnostic-app](Jupyter_Notebooks_TapisAppsOpenSees/tapis_discoverApp_Designsafe_Agnostic_App.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_TapisAppsOpenSees/tapis_discoverApp_Designsafe_Agnostic_App.ipynb' target='_blank'>Open in JupyterHub</a></sub>
- [Run Tapis Apps](Docs_MD_Tapis/runTapisApp.md)
  - [Step-by-Step OpenSees App](Jupyter_Notebooks_TapisAppsOpenSees/tapis_submitJob_DSapp_OpenSees_Detailed.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_TapisAppsOpenSees/tapis_submitJob_DSapp_OpenSees_Detailed.ipynb' target='_blank'>Open in JupyterHub</a></sub>
- [Run OpenSees-Express App](Jupyter_Notebooks_TapisAppsOpenSees/tapis_submitJob_DSapp_OpenSees_Compact_OpsExpress.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_TapisAppsOpenSees/tapis_submitJob_DSapp_OpenSees_Compact_OpsExpress.ipynb' target='_blank'>Open in JupyterHub</a></sub>
- [Run OpenSeesMP App](Jupyter_Notebooks_TapisAppsOpenSees/tapis_submitJob_DSapp_OpenSees_Compact_OpsMP.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_TapisAppsOpenSees/tapis_submitJob_DSapp_OpenSees_Compact_OpsMP.ipynb' target='_blank'>Open in JupyterHub</a></sub>
- [Run DS OpenSeesPy App](Docs_MD_Tapis/OpenSeesPy_App_RUN.md)
  - [Run OpenSeesPy App](Jupyter_Notebooks_TapisAppsOpenSees/DSOpenSeesPy_App_SUBMITjob.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_TapisAppsOpenSees/DSOpenSeesPy_App_SUBMITjob.ipynb' target='_blank'>Open in JupyterHub</a></sub>
- [Run DS Agnostic App](Docs_MD_Tapis/DSagnosticApp_OpenSees_RUN.md)
  - [Run Any OpenSees using DS Agnostic App](Jupyter_Notebooks_TapisAppsOpenSees/DSagnostic_App_anyOpenSees_SUBMITjob.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_TapisAppsOpenSees/DSagnostic_App_anyOpenSees_SUBMITjob.ipynb' target='_blank'>Open in JupyterHub</a></sub>

## TOC
