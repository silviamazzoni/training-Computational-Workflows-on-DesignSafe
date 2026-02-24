# Job Attrib. vs App Param.
***Understanding Job Submission Attributes vs. App Parameters***

When you submit a job to Tapis, you send a **job request object** (JSON). This object includes two kinds of information:

1.  General job settings (like job name, queue, and resource configuration)
 **Job-level attributes** — general metadata about how the job should be run (**resource configuration**)

2. Input files and parameter values defined by the app
 **App-level inputs and parameters** — specific values defined in the app template (e.g., script files, settings). **App Parameters** are used to pass in configuration values—such as numbers, flags, or options—that control how the app behaves. Parameters are also defined in the app’s app-definition.json file and made available to the wrapper script just like inputs.


But here’s the key distinction:

| **Field Type**     | **Used For**                                     | **Defined In**                                      |
| ------------------ | ------------------------------------------------ | --------------------------------------------------- |
| **Job attributes** | Scheduling, archiving, naming, resource requests | Part of the job request                             |
| **App parameters** | Controlling program behavior (flags, values)     | Defined in the app template (`app-definition.json`) |



## So What About Processors and Memory?

This is where the confusion between attributes and parameters often happens:

* **`nodeCount`, `processorsPerNode`, `memoryPerNode`**
  → These are **job-level attributes**. They are interpreted by the Tapis system to request resources from the execution system (e.g., SLURM).

* **`numProcessors` or `np`** (often defined as an app parameter)
  → This is a **separate app parameter** that controls how your script behaves (e.g., how many MPI processes to launch).

They’re **related**, but not the same. You often need to coordinate them:

* Ask for enough processors in the job attributes
* Then tell your wrapper how many processes to use via a parameter

This is important when you are running more than one concurrent application within the same SLURM job.

---

## Relationship Between Job Request Components

```
        +----------------------------+
        |       Job Submission      |
        +----------------------------+
        |                            |
        | 1. Job-Level Attributes    |
        |    - name                 |
        |    - appId                |             +-------------------+             +------------------------+
        |    - nodeCount            |             |    Tapis App      |             |     Wrapper Script     |
        |    - processorsPerNode    |    --->     |  (Template logic) |    --->     |  (e.g. app-wrapper.sh) |
        |    - memoryPerNode        |             +-------------------+             +------------------------+
        |    - archive, queue, etc. |             
        |                            |
        | 2. App Inputs & Parameters |
        |    - inputScript (file)   |
        |    - numProcessors (value)|
        |    - dampingRatio (value) |
        |                            |
        +----------------------------+

```

---

## Real Example

### **Job request** (user-supplied at runtime)

```json
{
  "name": "run-opensees",
  "appId": "openseesmp-3.5.0",
  "nodeCount": 1,
  "processorsPerNode": 4,
  "inputs": {
    "inputScript": "agave://designsafe.storage/path/model.tcl"
  },
  "parameters": {
    "numProcessors": "4"
  }
}
```

### **Wrapper script**

```bash
ibrun -np ${numProcessors} OpenSeesMP ${inputScript}
```

Here:

* `processorsPerNode` ensures the job requests 4 cores on the system
* `numProcessors` is passed into the app and used in the MPI command



## Best Practice

Always define both:

* **Job attributes**: so your job runs with the right amount of resources
* **App parameters**: so your script knows how to use those resources

This dual setup keeps Tapis flexible while still giving you full control.


Here’s a clean, user-friendly table that summarizes the key differences between **job submission attributes** and **app parameters**, including where they’re defined, how they’re used, and common examples — perfect for dropping into your documentation alongside the figure.



## Table: Job Attributes vs. App Parameters

| **Feature**                    | **Job Submission Attribute**                                       | **App Parameter**                                           |
| ------------------------------ | ------------------------------------------------------------------ | ----------------------------------------------------------- |
| **Purpose**                    | Tells Tapis how to run the job on the system                       | Tells the app how to behave during execution                |
| **Defined in**                 | Job request (JSON object submitted at runtime)                     | App template (`app-definition.json`)                        |
| **Evaluated by**               | Tapis system (e.g., scheduler, job handler)                        | Wrapper script (via variable substitution)                  |
| **Appears in wrapper?**        | Not automatically                                                  | Yes — as `${paramId}`                                       |
| **Examples**                   | `nodeCount`, `processorsPerNode`, `maxRunTime`, `archive`, `queue` | `numProcessors`, `useDamping`, `solverType`, `writeOutputs` |
| **Data type**                  | Strings, numbers, booleans, arrays                                 | Strings, numbers, booleans, enumerations, flags             |
| **Used for resource control?** |   Yes (e.g., SLURM or batch settings)                              |  Sometimes (e.g., to construct `ibrun -np`)               |
| **Used for command logic?**    |   No                                                               |  Yes                                                       |
| **Required?**                  | Some are required (e.g., `name`, `appId`)                          | Depends on the app’s design                                 |



## Summary

* Use **job submission attributes** to define where and how a job runs.
* Use **app parameters** to control what your script does and how it runs.
* When running parallel apps (like OpenSeesMP), you often set both:

  * Ask Tapis for the right number of processors (`processorsPerNode`)
  * Pass that value to your wrapper script using an app parameter (`numProcessors`)



## Job Submission Attributes

These fields are not app parameters. They are **global job settings** used by Tapis itself to manage scheduling, queuing, resource allocation, and archiving.

Let’s look at them by category:

| Attribute           | What it controls                        | Where it comes from                    |
| ------------------- | --------------------------------------- | -------------------------------------- |
| `name`              | A label for your job                    | Required in every submission           |
| `appId`             | The ID of the app you want to run       | Matches a registered Tapis App         |
| `batchQueue`        | Which queue on the cluster to submit to | Optional override (else auto-selected) |
| `nodeCount`         | Number of nodes to request              | Optional override                      |
| `processorsPerNode` | Cores per node                          | Optional override                      |
| `memoryPerNode`     | Memory per node (e.g., `8GB`, `128GB`)  | Optional override                      |
| `maxRunTime`        | Walltime (e.g., `02:00:00`)             | Optional override                      |
| `notifications`     | URLs to send updates to                 | Optional                               |
| `archive`           | Whether to archive the results          | Optional (default is usually `true`)   |
| `archiveSystem`     | Storage system to save results to       | Optional                               |
| `archivePath`       | Where to place archived outputs         | Optional                               |



## How This Differs From App Parameters

App **parameters** (defined in `app-definition.json`) are specific to that app’s logic. For example:

* `numProcessors`
* `analysisType`
* `useRayleighDamping`

These are passed into the **wrapper script** and affect how the application runs.

By contrast, job-level fields like `nodeCount` and `memoryPerNode` tell Tapis how to request resources from the scheduler — they don’t appear in the wrapper script (unless you manually inject them using environment variables or app parameters).



## Summary

* App **parameters** control how your program runs (and are defined inside the app).
* Job **submission attributes** control how Tapis manages your job (resources, queue, archiving).
* Both are part of the full job request, but they serve very different purposes.

