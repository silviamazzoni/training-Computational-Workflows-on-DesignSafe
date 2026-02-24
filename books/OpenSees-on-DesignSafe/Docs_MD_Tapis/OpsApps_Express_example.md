# Example

To submit a job to the **OpenSees-EXPRESS** Tapis app using **Tapipy**, you’ll need to construct a Python dictionary with the required fields and then call the *submitJob* method. Below is a complete example tailored for this app, using the fields defined in its *app.json*.



## Example: Tapipy Job Submission to OpenSees-EXPRESS

```python
from tapipy.tapis import Tapis

# Authenticate (example assumes TACC tenant)
t = Tapis(base_url='https://tacc.tapis.io',
          username='your-username',
          password='your-password',
          account_type='password',
          tenant_id='tacc')
t.authenticate()

# Define job input
job_body = {
    "name": "opensees_express_run_01",
    "appId": "opensees-express",
    "inputs": {},
    "parameterSet": {
        "envVariables": [
            {"key": "mainProgram", "value": "OpenSees"},
            {"key": "tclScript", "value": "my_model.tcl"}
        ]
    },
    "fileInputs": [
        {
            "name": "Input Directory",
            "sourceUrl": "agave://designsafe.storage.default/MyProject/InputFolder",
            "targetPath": "."
        }
    ],
    "archive": True,
    "archiveSystemId": "designsafe.storage.default",
    "archivePath": "MyProject/Results/${JobName}"
}

# Submit the job
job = t.jobs.submitJob(body=job_body)

# View job info
print("Submitted job:", job.id)
```



## What You Need to Provide

| Field             | Description                                                                                   |
| ----------------- | --------------------------------------------------------------------------------------------- |
| *name*            | A name for your job                                                                           |
| *appId*           | Must be *opensees-express*                                                                    |
| *fileInputs*      | Points to a directory on a Tapis storage system (must include your *.tcl* and required files) |
| *mainProgram*     | One of: *OpenSees*, *OpenSeesSP*, or *OpenSeesMP*                                             |
| *tclScript*       | Name of the *.tcl* file to run from within the input directory                                |
| *archive*         | Set to *True* to save outputs                                                                 |
| *archiveSystemId* | Typically *designsafe.storage.default*                                                        |
| *archivePath*     | Where outputs will be stored in your project directory                                        |

