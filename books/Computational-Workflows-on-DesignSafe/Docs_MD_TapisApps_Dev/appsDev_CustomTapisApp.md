# Creating a Custom Tapis App
***Create and Run a Custom App on DesignSafe Using TACC Modules (No Docker)***

This is a **comprehensive, unified guide**: it walks you through creating a **custom HPC-enabled Tapis app on DesignSafe** that uses **TACC’s environment modules (not Docker)**, and is launchable through both **code (Python + Tapipy)** and the **DesignSafe GUI**.


This guide ties together:

* Tapis-based app registration and job management
* Module-based (non-container) execution on TACC resources
* DesignSafe-specific deployment and GUI launching

This guide helps you define a reusable, shareable app that:

* Runs on **TACC HPC systems** like **Stampede3 or Frontera**
* Uses **modules** (like *module load python*, *OpenSees*, etc.)
* Can be launched from either the **DesignSafe GUI** or **Tapipy in Python**

---

## Prerequisites

* A [DesignSafe account](https://www.designsafe-ci.org)
* Basic knowledge of Python and shell scripting
* Access to a TACC execution system (e.g., *stampede3*)
* Installed tools:

  * Python environment with *tapipy*
  * Optionally: *tapis-cli-ng* for terminal-based registration

---

:::{dropdown} Step 1: Set Up Your App Directory

Structure your folder like this:

```
my-awesome-app/
├── run_analysis.py       # Your Python script
├── wrapper.sh            # Wrapper to load modules and run the script
├── app-definition.json   # Tapis app definition (for GUI + CLI)
```

::: 

:::{dropdown} Step 2: Your Python Code (*run_analysis.py*)

Example script:

```python
import sys

if len(sys.argv) != 2:
    print("Usage: python run_analysis.py <input_file>")
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    content = f.read()

print("=== File Contents ===")
print(content)
```

::: 

:::{dropdown} Step 3: Wrapper Script (*wrapper.sh*)

This script is executed on the HPC system.

```bash
#!/bin/bash
cd $WORK/$JOB_NAME

# Load the necessary environment modules
module load python/3.9

# Run your Python script using an input file provided by the user
python run_analysis.py "$input_file"
```

Make it executable:

```bash
chmod +x wrapper.sh
```

::: 

:::{dropdown} Step 4: Tapis App Definition (*app-definition.json*)

```json
{
  "id": "my-awesome-app-1.0",
  "name": "My Awesome App",
  "version": "1.0",
  "executionSystem": "designsafe.community.execution",
  "deploymentPath": "apps/my-awesome-app/1.0",
  "templatePath": "wrapper.sh",
  "executionType": "HPC",
  "runtime": "LINUX",
  "jobType": "BATCH",
  "parallelism": "SERIAL",
  "maxJobs": 10,
  "defaultMemory": "2GB",
  "defaultProcessors": 1,
  "defaultNodes": 1,
  "defaultMaxRunTime": "00:30:00",
  "deploymentSystem": "designsafe.storage.default",
  "inputs": [
    {
      "id": "input_file",
      "details": {
        "label": "Input File",
        "description": "A file to process"
      },
      "required": true,
      "inputType": "URI"
    }
  ],
  "parameters": [],
  "outputs": [
    {
      "id": "stdout.txt",
      "value": {
        "default": "stdout.txt"
      }
    }
  ],
  "tags": ["custom", "python", "designsafe"]
}
```

::: 

:::{dropdown} Step 5: Upload to DesignSafe/TACC

Upload your app files:

```bash
scp -r my-awesome-app/ yourusername@login.designsafe-ci.org:/work/apps/my-awesome-app/1.0
```

Or via the **DesignSafe Data Depot** → move the files to:

```
/work/apps/my-awesome-app/1.0
```

::: 

:::{dropdown} Step 6: Register the App via Tapis CLI (Optional)

If you prefer CLI:

```bash
pip install tapis-cli-ng
tapis auth login
tapis apps create -F app-definition.json
tapis apps list | grep my-awesome-app
```

::: 

:::{dropdown} Step 7: Register and Use the App in Python with Tapipy

**Authenticate and upload your files (same as above)**

```python
from tapipy.tapis import Tapis
import json

client = Tapis(
    base_url="https://designsafe.dev.tapis.io",  # or production URL
    username="your-username",
    password="your-password",
    tenant_id="designsafe"
)
client.get_tokens()

# Register the app
with open("app-definition.json") as f:
    app_def = json.load(f)

client.apps.createAppVersion(body=app_def)
```

::: 

:::{dropdown} Step 8: Upload an Input File

```python
with open("example_input.txt", "rb") as f:
    client.files.insert(
        systemId="designsafe.storage.default",
        path="input/example_input.txt",
        file=f
    )
```

::: 

:::{dropdown} Step 9: Submit a Job from Python

```python
job = client.jobs.submitJob(body={
    "name": "my-first-designsafe-job",
    "appId": "my-awesome-app-1.0",
    "appVersion": "1.0",
    "inputs": {
        "input_file": "tapis://designsafe.storage.default/input/example_input.txt"
    },
    "archive": True,
    "archiveSystemId": "designsafe.storage.default",
    "archivePath": "archive/my-awesome-output"
})
print("Job submitted:", job.id)
```

::: 

:::{dropdown} Step 10: Monitor and Download Output

```python
import time

while True:
    status = client.jobs.getJob(jobId=job.id).status
    print("Status:", status)
    if status in ["FINISHED", "FAILED", "CANCELLED"]:
        break
    time.sleep(10)

# Download output
client.jobs.getJobOutput(jobId=job.id, path="stdout.txt", destination="./stdout.txt")
```

::: 

:::{dropdown} Step 11: Launch from DesignSafe GUI

Once registered:

1. Go to **Workspace → Tools & Applications → Private Apps**
2. Click your app: “My Awesome App”
3. Fill in input fields (like file selectors)
4. Launch job – Tapis runs it on Stampede3 or Frontera
5. Results appear in your **Project Data** folder

:::

## Tips and Best Practices

* Use *parallelism: PARALLEL* for MPI or multithreaded jobs
* Use *$SCRATCH* for fast, temporary storage; *$WORK* for persistent storage
* Load any required tools (MATLAB, R, Python, etc.) with *module load* inside *wrapper.sh*
* Add *"helpURI"* to your app JSON for linking to documentation

---

## Summary

By following this guide, you've created a **DesignSafe app** that:

* Runs on **TACC’s HPC** with **no containers**
* Loads modules using *module load*
* Is callable via **GUI or Python**
* Provides full reproducibility and reusability for your workflows

