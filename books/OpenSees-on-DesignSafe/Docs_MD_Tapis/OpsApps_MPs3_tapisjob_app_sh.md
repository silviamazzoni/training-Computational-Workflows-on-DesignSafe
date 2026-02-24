# tapisjob_app.sh

This script runs on the Stampede3 compute node after the job is submitted via SLURM. It launches **OpenSeesMP using *ibrun***, which handles MPI-based parallel execution across multiple cores and nodes.

https://github.com/TACC/WMA-Tapis-Templates/blob/main/applications/opensees-mp/opensees-mp-s3/tapisjob_app.sh

## App-Definition File
:::{dropdown} **tapisjob_app.sh**
The following json was copied from github and may have changed.

```
set -x

BINARYNAME=$1
INPUTSCRIPT=$2
echo "INPUTSCRIPT is $INPUTSCRIPT"

TCLSCRIPT="${INPUTSCRIPT##*/}"
echo "TCLSCRIPT is $TCLSCRIPT"

cd "${inputDirectory}"

echo "Running $BINARYNAME"

ibrun $BINARYNAME $TCLSCRIPT
if [ ! $? ]; then
      echo "OpenSees exited with an error status. $?" >&2
      exit
fi

cd ..

```
:::

## What the Script Does

| Step                           | Purpose                                                                                  |
| ------------------------------ | ---------------------------------------------------------------------------------------- |
| *set -x*                       | Enables debug output in logs                                                             |
| Parses *$1* and *$2*           | Reads the OpenSees binary name and *.tcl* script filename from parameters                |
| *cd "${inputDirectory}"*       | Changes to the user’s input directory                                                    |
| *ibrun $BINARYNAME $TCLSCRIPT* | Runs OpenSeesMP in parallel across all assigned cores using SLURM's MPI launcher *ibrun* |
| Error check block              | Detects failure and exits cleanly if the job fails                                       |

## Line-by-Line Explanation

```bash
set -x
```

* Print every command before it's run — helpful for job log debugging.

```bash
BINARYNAME=$1
INPUTSCRIPT=$2
TCLSCRIPT="${INPUTSCRIPT##*/}"
```

* *$1* = *"OpenSeesMP"* from app parameters
* *$2* = name of the *.tcl* script
* *TCLSCRIPT* strips the path, keeping only the filename

```bash
cd "${inputDirectory}"
```

* Move into the uploaded directory — this is where the *.tcl* file and all required data should be.

```bash
ibrun $BINARYNAME $TCLSCRIPT
```

* The core of the job: runs OpenSeesMP using TACC’s *ibrun*, which launches an MPI job across the allocated nodes/cores.

```bash
if [ ! $? ]; then
    echo "OpenSees exited with an error status. $?" >&2
    exit
fi
```

* If OpenSeesMP exits with a nonzero status, this prints an error and stops the script. This makes failures visible to Tapis and the user.

## Summary

| Task            | Mechanism                                 |
| --------------- | ----------------------------------------- |
| Launch OpenSees | *ibrun OpenSeesMP model.tcl*              |
| Handle failure  | Exit if OpenSees crashes or returns error |
| Log output      | *set -x* prints all commands for tracing  |



