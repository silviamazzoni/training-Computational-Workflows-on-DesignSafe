# tapisjob_app.sh

This script is executed on the execution system when your Tapis job runs. <br>
It is responsible for launching the OpenSees simulation inside a container, using your uploaded input files and specified parameters.

This is the **runtime wrapper** script executed on the compute system after your Tapis job starts. It:

* Runs an OpenSees simulation **inside an Apptainer (Singularity) container**
* Mounts your input directory into the container
* Executes your chosen OpenSees binary (e.g., *OpenSees*, *OpenSeesSP*, or *OpenSeesMP*)
* Reports the job’s exit status to Tapis

https://github.com/TACC/WMA-Tapis-Templates/blob/main/applications/opensees-express/tapisjob_app.sh

:::{dropdown} tapisjob_app.sh
The following json was copied from github and may have changed.
```
set -x

apptainer run \
    --cleanenv \
    --bind "${inputDirectory}":/data \
    docker://taccaci/opensees:latest \
    /bin/sh -c \
        "cd /data; ${mainProgram} < /data/$tclScript"

EXITCODE=$?
if [ $EXITCODE -ne 0 ]; then
    # Command failed
    echo "Apptainer container exited with an error status. $EXITCODE" >&2

    # https://tapis.readthedocs.io/en/latest/technical/jobs.html#monitoring-the-application
    echo $EXITCODE > ${_tapisExecSystemOutputDir}/tapisjob.exitcode
fi

```
:::

##  What the Script Does

| Step                                          | Purpose                                                                                                                |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| *set -x*                                      | Enables debugging — prints each command as it runs (helpful for logs)                                                  |
| *apptainer run ...*                           | Launches a containerized OpenSees job using [Apptainer](https://apptainer.org/)                                        |
| *--bind "${inputDirectory}":/data*            | Mounts the input directory (uploaded via Tapis) into the container at */data*                                          |
| *docker://taccaci/opensees:latest*            | Uses the latest OpenSees Docker image published by TACC                                                                |
| *cd /data; ${mainProgram} < /data/$tclScript* | Runs your specified OpenSees binary (e.g., *OpenSees*, *OpenSeesSP*, or *OpenSeesMP*) on your uploaded *.tcl* script   |
| *EXITCODE=$?*                                 | Captures the success/failure code of the simulation                                                                    |
| Error handling block                          | If the job fails, logs the exit code and writes it to a file named *tapisjob.exitcode* so Tapis can track job failures |

###  Why This Matters

* This wrapper isolates all software dependencies using containers, ensuring reproducibility
* You don’t need to write job scripts — this handles it for you
* It’s portable: can run on any TACC/DesignSafe system that supports Apptainer
* Tapis uses the exit code file to determine if your simulation ran successfully




## Line-by-Line Explanation

```bash
set -x
```

* Enables **debug mode**: prints each command as it's executed, useful for troubleshooting in job logs.

---

```bash
apptainer run \
    --cleanenv \
    --bind "${inputDirectory}":/data \
    docker://taccaci/opensees:latest \
    /bin/sh -c \
        "cd /data; ${mainProgram} < /data/$tclScript"
```

This block runs the **OpenSees simulation** inside a container. Here's what each part does:

| Part                                          | Description                                                                                                                                 |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| *apptainer run*                               | Runs a containerized app using [Apptainer](https://apptainer.org/) (formerly Singularity), common in HPC environments                       |
| *--cleanenv*                                  | Strips the host's environment to avoid conflicts inside the container                                                                       |
| *--bind "${inputDirectory}":/data*            | Mounts your input files (uploaded via Tapis) into the container at */data*                                                                  |
| *docker://taccaci/opensees:latest*            | Pulls the latest version of the official OpenSees Docker image from Docker Hub                                                              |
| */bin/sh -c "..."*                            | Tells the container to run a shell command:                                                                                                 |
| *cd /data; ${mainProgram} < /data/$tclScript* | Changes into the input folder, then runs the OpenSees executable (*OpenSees*, *OpenSeesSP*, or *OpenSeesMP*) on the specified *.tcl* script |

→ *${mainProgram}* and *$tclScript* are populated from the **job parameters** (as defined in the *app.json*).

---

```bash
EXITCODE=$?
```

* Captures the exit status (*0* = success, anything else = error) of the previous command (i.e., the simulation run).

---

```bash
if [ $EXITCODE -ne 0 ]; then
    # Command failed
    echo "Apptainer container exited with an error status. $EXITCODE" >&2

    # https://tapis.readthedocs.io/en/latest/technical/jobs.html#monitoring-the-application
    echo $EXITCODE > ${_tapisExecSystemOutputDir}/tapisjob.exitcode
fi
```

* If the job **fails**, this block:

  * Prints an error message to *stderr*
  * Writes the numeric exit code to a file named *tapisjob.exitcode* in the output folder
  * This is useful because Tapis uses this file to determine whether the job completed successfully



##  Summary: What This Wrapper Does

| Task            | Mechanism                                      |
| --------------- | ---------------------------------------------- |
| Mounts inputs   | *--bind "${inputDirectory}":/data*             |
| Runs simulation | *${mainProgram} < $tclScript* inside container |
| Reports errors  | Writes exit code if the job fails              |

This design allows OpenSees to be run **without installing anything on the host**, and ensures **consistency and reproducibility** by running in a clean containerized environment.





