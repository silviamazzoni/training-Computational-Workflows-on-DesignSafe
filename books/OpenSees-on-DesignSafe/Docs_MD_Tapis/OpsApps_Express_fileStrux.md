# App Structure
***Understanding the OpenSees-Express Tapis App Structure***

The **OpenSees-Express** app is a streamlined Tapis application designed to run small, sequential OpenSees jobs on a dedicated **virtual machine (VM)** instead of an HPC cluster. It is lightweight, fast to launch, and ideal for testing or small-scale modeling.

Unlike OpenSeesMP, the Express app does not use *profile.json* or load software modules. Instead, it runs inside a **Docker container** defined at build time. The app is defined by three main files that control its behavior and runtime setup.

You can acces the app template in the TACC repo: https://github.com/TACC/WMA-Tapis-Templates/tree/main/applications/opensees-express

### The three core files are:

* **app.json** – Defines the app interface and inputs. This tells Tapis what input files are required and how to present the app in the DesignSafe web portal. It also specifies which Docker image to run.

* **tapisjob_app.sh** – This is the runtime script executed inside the container. It launches OpenSees using the main input file provided by the user, and reports the job’s status back to Tapis.

* **Dockerfile** – Describes the container environment. It installs OpenSees and any dependencies into a portable image that can run on the VM. This ensures consistent software behavior regardless of where the job is launched.

Together, these files let OpenSees-Express run OpenSees simulations in a containerized VM environment, making it easy to use without requiring access to a full HPC system.


```{dropdown} Dockerfile: Defining the OpenSees Runtime Environment

The *Dockerfile* in the *OpenSees-express* app template is responsible for building a container image that includes everything needed to run OpenSees. In this case, it creates a minimal environment using:

* A **Debian-based image** for stability and simplicity
* A **download-and-install step** for the OpenSees binary from a trusted release
* A default entrypoint that runs a *.tcl* script using OpenSees

**Key Features**

Here’s what the Dockerfile does at a high level:

1. **Starts from a slim Linux base**

    FROM debian:bullseye-slim

2. **Installs dependencies like curl and unzip**
   These tools are needed to fetch and extract the OpenSees binary.

    RUN apt-get update && apt-get install -y curl unzip

3. **Downloads and installs OpenSees**
   It fetches a specific Linux binary release from the NEESHub GitHub archive.

    RUN curl -L -o OpenSees.zip https://github.com/...

4. **Sets up the OpenSees executable in the container's path**
   So it can be called directly in the wrapper.

5. **Defines a simple entrypoint**
   Which lets the container run a user-provided *.tcl* file:

    ENTRYPOINT ["OpenSees"]
    CMD ["input.tcl"]

This makes the container highly portable and easy to reuse. It runs OpenSees as soon as it's launched, using a default input file unless otherwise specified.
```



```{dropdown} app.json: Declaring the App Interface for Tapis

The *app.json* file (sometimes called *app-definition.json* in other apps) is the **formal declaration** of the app to the Tapis system. It defines:

* What this app does
* What inputs it expects
* What parameters it accepts
* How the system should run it

In *OpenSees-express*, this file is intentionally minimal, reflecting the simplicity of the container design.

* **Key Components of *app.json***

    | Field              | Description                                                     |
    | ------------------ | --------------------------------------------------------------- |
    | *id*               | Unique name for the app (e.g., *"opensees-express-1.0"*)        |
    | *name*             | Human-readable name                                             |
    | *version*          | App version                                                     |
    | *executionSystem*  | The Tapis system where the job will run (must support Docker)   |
    | *deploymentPath*   | Where the app files will live on the system                     |
    | *deploymentSystem* | Where the app is stored (usually the same as *executionSystem*) |
    | *parallelism*      | Set to *"SERIAL"* — this app does not use MPI                   |
    | *executionType*    | Set to *"CONTAINER"* — indicates it runs inside Docker          |
    | *container*        | Defines the Docker image and entrypoint                         |
    | *inputs*           | Declares the input file the user must provide (*inputFile*)     |
    | *outputs*          | Declares expected output files to archive                       |
    | *parameters*       | None in this app (it just runs the *.tcl* script as-is)         |



* **What the User Must Provide**

    This app has **one required input**:
    
        {
          "id": "inputFile",
          "details": {
            "label": "OpenSees Input File",
            "description": "A .tcl input file for OpenSees"
          }
        }
    
    
    No parameters are required — the app simply runs OpenSees on the provided *.tcl* script using the default container entrypoint.



* **Why It’s Clean and Simple**

    Because the app is self-contained and runs a single *.tcl* script with no parameters or custom logic, the *app.json* is:
    
    * Easy to register
    * Easy to use in automated workflows
    * Great for demonstration, testing, or education


```



```{dropdown}  tapisjob_app.sh: The Runtime Wrapper

The *tapisjob_app.sh* script is a **shell wrapper** that runs inside the container at job runtime. Tapis copies this script to the working directory and uses it as the job’s entrypoint command. Its job is simple: run the OpenSees application using the provided input file.

Since the Docker image already defines *OpenSees* as the default executable (*ENTRYPOINT*), this script acts as a **lightweight interface layer** between the Tapis system and the OpenSees runtime.

* **What It Does**

    Here’s what the script does, step by step:
    
        #!/bin/bash
        set -e
        
        # Run OpenSees with the input file path
        OpenSees $inputFile
    
    
    That’s it! But let’s break down why this matters:

* **Key Notes**

    * *set -e* ensures the script exits immediately if any command fails, preventing silent errors.
    * *$inputFile* is an environment variable set by Tapis, based on the user’s submitted input.
    * *OpenSees* refers to the executable made available by the Docker container.
    
    This wrapper ensures that no matter where or how the app is launched, the behavior is consistent: it will always run OpenSees on the given *.tcl* input file.

```
