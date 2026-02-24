# get_tapis_job_all_files()
***get_tapis_job_all_files(t, jobUuid, displayIt=10, local_base_dir=False, overwrite=False)***


##  Overview

The *get_tapis_job_all_files* function is a powerful utility for working with Tapis jobs.
It recursively explores all output files produced by a given Tapis job, returning:

* **Relative local-style file paths** (helpful for mirroring directory structures when downloading).
* **Full absolute Tapis system paths** (needed for direct API calls or future metadata checks).
* **Raw item metadata** returned by Tapis (includes type, size, modification times, etc.).
* **Total file count**.

Additionally, it can **automatically download** all found files into a local directory, preserving the directory hierarchy of the remote Tapis job.


##  Function Signature

```python
get_tapis_job_all_files(
    t, jobUuid,
    displayIt=10,
    local_base_dir=False,
    overwrite=False
)
```



##  Parameters

| Parameter        | Type                               | Description                                                                                                                                                                                                                                                                                      |
| ---------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| *t*              | *Tapis*                            | An authenticated Tapis client (typically from *connect_tapis()*).                                                                                                                                                                                                                                |
| *jobUuid*        | *str*                              | The UUID of the Tapis job whose outputs you wish to list or download.                                                                                                                                                                                                                            |
| *displayIt*      | *bool* or *int*, optional          | Controls printing of the directory tree: <ul><li>*False* or *0*: silent (prints nothing).</li><li>*True* or *1*: prints all files in all directories.</li><li>*>=2*: prints up to *displayIt* files per directory, then shows a message indicating suppressed output.</li></ul> Default is *10*. |
| *local_base_dir* | *bool*, *None*, or *str*, optional | Determines download behavior: <ul><li>*False* or *None*: does not download (just lists).</li><li>*True*: downloads files into *./OutFiles_{jobUuid}* by default.</li><li>*str*: downloads files into the specified directory.</li></ul> Default is *False*.                                      |
| *overwrite*      | *bool*, optional                   | If *True*, existing local files will be overwritten. Default is *False* (skips existing files).                                                                                                                                                                                                  |


##  Returns

Returns a *dict* with:

| Key           | Type        | Description                                                                    |
| ------------- | ----------- | ------------------------------------------------------------------------------ |
| *'Nfiles'*    | *int*       | Total number of files found (excluding directories).                           |
| *'LocalPath'* | *list[str]* | Relative file paths (suitable for recreating the directory structure locally). |
| *'FullPath'*  | *list[str]* | Absolute paths on the Tapis system.                                            |
| *'Items'*     | *list*      | Raw Tapis file metadata objects (contains type, size, lastModified, etc.).     |



##  Behavior Summary

| *local_base_dir* value | What happens                                                        |
| ---------------------- | ------------------------------------------------------------------- |
| *False* or *None*      | Only lists files, no downloads performed.                           |
| *True*                 | Downloads files into a default local folder *./OutFiles_{jobUuid}*. |
| *"mydir"* (string)     | Downloads files into the specified directory.                       |

All downloads **preserve the original remote directory structure**.



##  Example Usage

###  Just list the files, print up to 5 per directory

```python
outputs = get_tapis_job_all_files(t, jobUuid, displayIt=5)
print(outputs['Nfiles'], "files found.")
```

###  List all files silently

```python
outputs = get_tapis_job_all_files(t, jobUuid, displayIt=False)
```


###  Download into default folder

```python
outputs = get_tapis_job_all_files(t, jobUuid, local_base_dir=True)
```

This will download all files into a local folder:

```
./OutFiles_{jobUuid}/results/output.txt
./OutFiles_{jobUuid}/logs/run.log
...
```



###  Download into a custom folder, overwriting any existing files

```python
outputs = get_tapis_job_all_files(
    t, jobUuid, 
    local_base_dir="MyDownloads",
    overwrite=True
)
```


##  Notes

* The *'Items'* list provides the original Tapis metadata objects for each file, which can include:

  * type (file or directory)
  * length (bytes)
  * lastModified
* Downloads are streamed in binary, and this function creates all necessary subfolders under *local_base_dir*.
* If *overwrite=False* (default), existing local files are skipped with a message.


**Recommended next steps:**

* Use *'LocalPath'* + *'FullPath'* pairs for further file processing, logs, or reporting.
* Integrate with data analysis pipelines that take a structured folder of downloaded results.

Absolutely! 🎉 Here’s a **beautifully structured Quickstart panel** you can drop into your **Jupyter Book (or any markdown docs)**.
It shows side-by-side typical use cases, so users quickly see how to leverage your function.

---

## Quickstart Panel: Using *get_tapis_job_all_files*

### Typical workflows

| Example                                                         | What it does                                                                                                                                             |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Just list files, print up to 5 per directory:**            | *python outputs = get_tapis_job_all_files(t, jobUuid, displayIt=5) print(f"Found {outputs['Nfiles']} files.") *                                          |
| **List all files without printing anything:**                | *python outputs = get_tapis_job_all_files(t, jobUuid, displayIt=False) *                                                                                 |
| **Download all files into default folder:**                  | *python outputs = get_tapis_job_all_files(t, jobUuid, local_base_dir=True) * <br>This creates *./OutFiles_{jobUuid}/...* preserving directory structure. |
| **Download into a custom folder, overwrite existing files:** | *python outputs = get_tapis_job_all_files(t, jobUuid, local_base_dir="MyResults", overwrite=True) *                                                      |

---

###  What’s returned?

You always get back a dictionary like:

```python
{
    'Nfiles': 42,
    'LocalPath': ['results/data.csv', 'logs/run.log', ...],
    'FullPath': ['/tapis/jobs/v2/job-outputs/.../data.csv', ...],
    'Items': [<TapisItem>, <TapisItem>, ...]
}
```

#### Use this to:

* Build download or analysis pipelines.
* Create logs of what was produced by your HPC jobs.
* Or simply verify that all expected outputs were generated.


###  Pro Tip

* Set *displayIt=10* to show only the first 10 files per directory (helps with large jobs).
* Change *overwrite=True* if you’re rerunning analyses and want to ensure fresh files.



#### Files
You can find these files in Community Data.

```{dropdown} get_tapis_job_all_files.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/get_tapis_job_all_files.py
:language: none
```
