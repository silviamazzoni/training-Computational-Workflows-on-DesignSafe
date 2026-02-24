# Tapis-App Structure

## Structure Overview

This template includes:

* **app-definition.json**: Describes the app’s metadata and links it to a system (like Frontera or Stampede3). It defines:

  * *deploymentSystem* and *executionSystem*
  * CLI-style *parameters* and *inputs*
  * Output handling rules

* **tapisjob_app.sh**: The actual launch script. It:

  * Loads the OpenSees module (or uses a container)
  * Builds the MPI run command (e.g., *ibrun OpenSeesMP*)
  * Moves inputs and manages outputs

* *README.md*: Provides guidance on how to install the app using the Tapis CLI or API.

You can learn more about Tapis Apps in the **Computational Workflows on DesignSafe** training document.

The following provide a working example of how to wrap the parallel version of OpenSees into a Tapis App.
* [OpenSeesExpress app template](https://github.com/TACC/WMA-Tapis-Templates/tree/main/applications/opensees-express) 
* [OpenSeesMP app template](https://github.com/TACC/WMA-Tapis-Templates/tree/main/applications/opensees-mp/opensees-mp-s3) 
