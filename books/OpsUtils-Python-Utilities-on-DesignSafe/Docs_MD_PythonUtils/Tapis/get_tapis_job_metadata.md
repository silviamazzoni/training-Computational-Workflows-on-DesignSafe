# get_tapis_job_metadata()
***get_tapis_job_metadata(t,jobUuid)***


Fetches metadata for a specified Tapis job and prints a structured summary including UUID, name, status, app ID, creation time, and archive location.
If the job has **completed**, it intelligently reconstructs the expected local archive directory path under *~/MyData/tapis-jobs-archive*, checks whether this directory exists, lists its contents, and returns all this information in a structured dictionary.

**Inputs:**

* *t* (*Tapis client object*):
  Authenticated Tapis client instance (from *tapis3* or *py-tapis*) used to query job details.
* *jobUuid* (*str*):
  UUID of the job to query.

**Outputs:**

* Returns a **dictionary** with keys:

  | Key         | Type           | Description                                          |
  | ----------- | -------------- | ---------------------------------------------------- |
  | local\_path | str or None    | Local archive directory path if finished, else None. |
  | exists      | bool           | True if the local directory exists.                  |
  | files       | list of str    | Files in the directory if it exists.                 |
  | message     | str (optional) | Message describing status if data not available.     |

**Behavior:**

* Prints a structured summary of job metadata.
* Carefully reconstructs local archive path to avoid hardcoded assumptions.
* Lists files if the local directory exists, or prints an explanatory message if not.

**Example usage:**

```python
result = get_tapis_job_metadata(t, "a1b2c3d4-5678-90ef-ghij-klmnopqrstuv")
if result["exists"]:
    print("Local data directory:", result["local_path"])
    print("Files:", result["files"])
else:
    print(result.get("message", "No data yet."))
```


#### Files
You can find these files in Community Data.

```{dropdown} get_tapis_job_metadata.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/get_tapis_job_metadata.py
:language: none
```

