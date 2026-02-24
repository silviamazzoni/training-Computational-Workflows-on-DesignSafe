# Table of Contents

## 
- [HOME](HOME.md)
- [Document Objectives](Docs_MD/Objectives.md)
  - [About This Document](Docs_MD/About.md)
  - [Prerequisites](Docs_MD/PreRequisites.md)
  - [Training Material](Docs_MD/TrainingMaterial.md)
- [DocSeries](Docs_MD/DocSeries.md)

## Computational Workflows
- [Workflow Systems](Docs_MD_Workflows/WorkflowSystems.md)
  - [Workflow Design](Docs_MD_Workflows/WorkflowDesign.md)
  - [Workloads](Docs_MD_Workflows/ComputationalWorkTypes.md)
  - [Workflow Types](Docs_MD_Workflows/WorkflowTypes.md)
- [Workflow Architecture](Docs_MD_Workflows/WorkflowArchitecture.md)
- [Execution Strategies](Docs_MD_Workflows/ExecutionStrategies.md)
  - [Execution Strategy Matrix](Docs_MD_Workflows/ExecutionStrategies_Matrix.md)

## SLURM Jobs
- [SLURM Jobs](Docs_MD_SLURM/README_SLURM.md)
- [How to Run a SLURM Job](Docs_MD_SLURM/SLURM_Run.md)
  - [Job Inputs](Docs_MD_SLURM/SLURM_Input.md)
  - [SLURM-Job Output](Docs_MD_SLURM/SLURM_OutErrFiles.md)
- [SLURM-Job Workflow](Docs_MD_SLURM/SLURM_Workflow.md)
- [Resources & Runtime](Docs_MD_SLURM/resources_and_runtime_in_SLURM.md)
  - [Login vs Execution Nodes](Docs_MD_SLURM/execution_vs_login_node_in_SLURM.md)
- [Job Scheduling](Docs_MD_SLURM/SLURM_Scheduling.md)
- [Ranks in MPI Jobs](Docs_MD_SLURM/MPIRanks.md)
- [PyLauncher](Docs_MD_SLURM/PyLauncher.md)
  - [Common Mistakes](Docs_MD_SLURM/PyLauncher_commonMistakes.md)
- [Job Arrays vs Launcher](Docs_MD_SLURM/SLURM_JobArray_vs_Launcher.md)
  - [Parameter Sweeps](Docs_MD_SLURM/SLURMmanual_ParameterSweep.md)
  - [Python JobArray def](Docs_MD_SLURM/SLURMmanual_PythonDef_JobArray.md)
  - [Python Launcher def](Docs_MD_SLURM/SLURMmanual_PythonDef_Launcher.md)

## Tapis
- [Scaling Jobs with Tapis](Docs_MD_Tapis/job_automation.md)
- [Tapis Overview](Docs_MD_Tapis/tapis_intro.md)
- [Interfacing with Tapis](Docs_MD_Tapis/tapis_interfacing.md)
- [Tapis Jobs](Docs_MD_Tapis/tapis_jobs.md)
  - [SLURM and Tapis](Docs_MD_Tapis/slurm_and_tapis.md)
  - [Tapis as Automation](Docs_MD_Tapis/tapis_SLURM_job.md)

## Tapis Apps
- [Tapis Apps](Docs_MD_TapisApps/tapis_apps.md)
  - [Tapis-App Glossary](Docs_MD_Tapis/tapis_glossary.md)
- [Tapis-App Types](Docs_MD_TapisApps/tapis_app_types.md)
  - [Execution Flows](Docs_MD_TapisApps/tapis_app_types_FlowCharts.md)
  - [What Is Apptainer?](Docs_MD_TapisApps/tapis_apptainer.md)
- [Run a Tapis App](Docs_MD_TapisApps/tapis_app_submitProcess.md)
  - [Job Execution Details](Docs_MD_TapisApps/tapis_job_execution_details.md)
- [Tapis-Job Profiling](Docs_MD_TapisApps/tapis_jobProfiling.md)
- [Anatomy of a Tapis App](Docs_MD_TapisApps_Dev/Anatomy_TapisApp.md)
  - [app.json Schema](Docs_MD_TapisApps_Dev/appJson_schema.md)
    - [Job Attrib. vs App Param.](Docs_MD_TapisApps_Dev/JobAttributes_vs_AppParams.md)
    - [app.json vs profile.json](Docs_MD_TapisApps_Dev/appJson_profileJson.md)
  - [App Files](Docs_MD_TapisApps_Dev/TapisJobFiles.md)
    - [Sample App Files](Docs_MD_TapisApps_Dev/TapisJobFiles_samples.md)
  - [Scheduler Profile](Docs_MD_TapisApps_Dev/SchedulerProfile.md)
    - [Scheduler vs. envVariables](Docs_MD_TapisApps_Dev/SchedulerProfile_vs_envVariables.md)
- [Custom Tapis Apps](Docs_MD_TapisApps_Dev/PublicAndCustomApps.md)
  - [Tapis App Templates](Docs_MD_TapisApps_Dev/tapis_AppTemplates.md)
  - [MPI in Tapis Apps](Docs_MD_TapisApps_Dev/MPIinTapisApps.md)
  - [HPC Launchers](Docs_MD_TapisApps_Dev/Launchers.md)
  - [Best Practices](Docs_MD_TapisApps_Dev/tapis_appsDev_BestPractice.md)

## DesignSafe Tapis Apps
- [DesignSafe Tapis Apps](Docs_MD_TapisApps_DSapps/DSapps.md)
  - [OpenSees Apps](Docs_MD_TapisApps_DSapps/DSapps_OpenSees.md)
  - [OpenFOAM app](Docs_MD_TapisApps_DSapps/DSapps_OpenFOAM.md)
  - [ADCIRC app](Docs_MD_TapisApps_DSapps/DSapps_ADCIRC.md)
  - [Compare Apps](Docs_MD_TapisApps_DSapps/DSapps_Compare.md)
- [designsafe-agnostic-app](Docs_MD_TapisApps_DSapps/DSagnosticApp_README.md)
  - [AgnosticApp - Input Arguments](Docs_MD_TapisApps_DSapps/DSagnosticApp_Inputs.md)
  - [AgnosticApp - Quick Reference](Docs_MD_TapisApps_DSapps/DSagnosticApp_QuickReference.md)
  - [AgnosticApp - How to Choose Inputs](Docs_MD_TapisApps_DSapps/DSagnosticApp_GUIDE.md)

## Training Modules
- [PyLauncher TaskList](Jupyter_Notebooks_Misc/PyLauncherTaskList.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Misc/PyLauncherTaskList.ipynb' target='_blank'>Open in JupyterHub</a></sub>
- [HDF5 Quick Explorer](Jupyter_Notebooks_Misc/HDF5_Quick_Explorer.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Misc/HDF5_Quick_Explorer.ipynb' target='_blank'>Open in JupyterHub</a></sub>
- [tapis_train_setup](Docs_MD_Tapis/tapis_train_setup.md)
  - [Tapis Authentication](Jupyter_Notebooks_Tapis/tapisConnect_connectToTapis.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapisConnect_connectToTapis.ipynb' target='_blank'>Open in JupyterHub</a></sub>
  - [System Specifications](Jupyter_Notebooks_Tapis/tapisConnect_getSystemSpecs.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapisConnect_getSystemSpecs.ipynb' target='_blank'>Open in JupyterHub</a></sub>
  - [Establish TMS Credentials](Jupyter_Notebooks_Tapis/tapisConnect_establishSystemCredentials.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapisConnect_establishSystemCredentials.ipynb' target='_blank'>Open in JupyterHub</a></sub>
  - [Tapis Paths](Jupyter_Notebooks_Tapis/tapisConnect_tapisPaths.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapisConnect_tapisPaths.ipynb' target='_blank'>Open in JupyterHub</a></sub>
- [Query and Retrieve Jobs](Docs_MD_Tapis/tapis_train_queryJobs.md)
  - [Step 1: Explore All Jobs](Jupyter_Notebooks_Tapis/tapis_queryJobs_ExploreAllJobs.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapis_queryJobs_ExploreAllJobs.ipynb' target='_blank'>Open in JupyterHub</a></sub>
    - [Explore All Jobs](Jupyter_Notebooks_Tapis/tapis_getJobList_AllJobs.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapis_getJobList_AllJobs.ipynb' target='_blank'>Open in JupyterHub</a></sub>
    - [Filter Tapis Jobs](Jupyter_Notebooks_Tapis/tapis_getJobList_FilterJobs.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapis_getJobList_FilterJobs.ipynb' target='_blank'>Open in JupyterHub</a></sub>
  - [Step 2: Inspect Job](Jupyter_Notebooks_Tapis/tapis_queryJobs_InspectJob.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapis_queryJobs_InspectJob.ipynb' target='_blank'>Open in JupyterHub</a></sub>
    - [Job Status](Jupyter_Notebooks_Tapis/tapis_getJobMeta_JobStatus.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapis_getJobMeta_JobStatus.ipynb' target='_blank'>Open in JupyterHub</a></sub>
    - [Job Metadata](Jupyter_Notebooks_Tapis/tapis_getJobMeta_JobMetaData.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapis_getJobMeta_JobMetaData.ipynb' target='_blank'>Open in JupyterHub</a></sub>
    - [Job History](Jupyter_Notebooks_Tapis/tapis_getJobMeta_JobHistoryData.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapis_getJobMeta_JobHistoryData.ipynb' target='_blank'>Open in JupyterHub</a></sub>
  - [Step 3: Retrieve Output](Jupyter_Notebooks_Tapis/tapis_queryJobs_RetrieveOutput.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapis_queryJobs_RetrieveOutput.ipynb' target='_blank'>Open in JupyterHub</a></sub>
    - [Access Output Data](Jupyter_Notebooks_Tapis/tapis_getJobOutData_AccessData.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapis_getJobOutData_AccessData.ipynb' target='_blank'>Open in JupyterHub</a></sub>
    - [List All Job Output](Jupyter_Notebooks_Tapis/tapis_getJobOutData_OutputFiles_Metadata.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapis_getJobOutData_OutputFiles_Metadata.ipynb' target='_blank'>Open in JupyterHub</a></sub>
    - [Download All Job Output](Jupyter_Notebooks_Tapis/tapis_getJobOutData_OutputFiles_Download.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapis_getJobOutData_OutputFiles_Download.ipynb' target='_blank'>Open in JupyterHub</a></sub>
    - [Explore Jobs Interactively](Jupyter_Notebooks_Tapis/tapis_getJobList_ExploreJobsInteractive.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_Tapis/tapis_getJobList_ExploreJobsInteractive.ipynb' target='_blank'>Open in JupyterHub</a></sub>
  - [Cancel Tapis Job](Docs_MD_Tapis/tapis_train_cancelJob.md)
- [Explore Tapis Apps](Docs_MD_Tapis/tapis_apps_explore.md)
  - [List Tapis Apps](Jupyter_Notebooks_TapisApps/tapis_getApps_List.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_TapisApps/tapis_getApps_List.ipynb' target='_blank'>Open in JupyterHub</a></sub>
  - [Get Tapis App Schema](Jupyter_Notebooks_TapisApps/tapis_getApps_Schema.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_TapisApps/tapis_getApps_Schema.ipynb' target='_blank'>Open in JupyterHub</a></sub>
  - [designsafe-agnostic-app](Jupyter_Notebooks_TapisApps/tapis_discoverApp_Designsafe_Agnostic_App.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_TapisApps/tapis_discoverApp_Designsafe_Agnostic_App.ipynb' target='_blank'>Open in JupyterHub</a></sub>
- [Run DS Agnostic App](Docs_MD_TapisApps_DSapps/DSagnosticApp_RUN.md)
  - [Machine-Learning Example](Jupyter_Notebooks_AgnosticApp_MLexample/DS_Agnostic_App_Submit_MLExample.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_AgnosticApp_MLexample/DS_Agnostic_App_Submit_MLExample.ipynb' target='_blank'>Open in JupyterHub</a></sub>
- [Creating a Custom Tapis App](Docs_MD_TapisApps_Dev/appsDev_CustomTapisApp.md)
  - [Custom App: opensees-mp-s3-clone](Jupyter_Notebooks_TapisAppsDev/custApp_opensees-mp-s3clone.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_TapisAppsDev/custApp_opensees-mp-s3clone.ipynb' target='_blank'>Open in JupyterHub</a></sub>
  - [Build A Custom Tapis App](Jupyter_Notebooks_TapisAppsDev/custApp_DesignSafe-Agnostic_A_BuildApp.ipynb)
      <sub>📂 <a href='https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/Jupyter_Notebooks_TapisAppsDev/custApp_DesignSafe-Agnostic_A_BuildApp.ipynb' target='_blank'>Open in JupyterHub</a></sub>

## TOC
