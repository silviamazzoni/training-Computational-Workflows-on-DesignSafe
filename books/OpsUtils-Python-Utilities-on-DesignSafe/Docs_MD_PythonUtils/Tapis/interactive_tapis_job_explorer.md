# interactive_tapis_job_explorer()
***interactive_tapis_job_explorer(t,JobsData_df)***

Launch an interactive, widget-driven interface to explore Tapis job data directly within a Jupyter Notebook.

This tool is ideal for reviewing computational jobs submitted to DesignSafe via the Tapis API, including metadata inspection, execution history, and output file management.

## Parameters

| Parameter     | Type               | Description                                                                                                                                                                                           |
| ------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **t**           | **Tapis** client     | An authenticated Tapis client object. Usually created using `OpsUtils.connect_tapis()`.                                                                                                               |
| **JobsData_df** | **pandas.DataFrame** | A DataFrame of Tapis jobs. Must include at least these columns:<br>*uuid*, *name*, *created*, *status*, *execSystemId*, *appId*.<br>If *'created_dt'* is not present, it is derived from *'created'*. |


## Features & Functionality

### Job Filtering

* Filter by:

  * **Status** (e.g., RUNNING, FINISHED, FAILED)
  * **Execution System**
  * **App ID**
  * **Creation Date Range**

### Job Sorting

* Sort jobs by any available column.
* Toggle ascending/descending order.
* Optional checkbox to show all rows.

### Job Selection

* Dropdown for selecting a job by UUID.
* Summary shown includes:

  * Job metadata
  * Execution history
  * Job step durations
  * Output file listing

###  Output File Management

#### All Outputs

* Lists and downloads all job output files.
* Downloads to `outputs_<jobUuid>` folder by default.
* Optional **overwrite checkbox**.

#### Individual File

* Dropdown to choose an individual output file.
* Buttons to:

  * **View** the file in a scrollable text box.
  * **Download** the file (with overwrite toggle).

##  Dependencies

This tool uses:

* `ipywidgets`
* `pandas`
* `datetime`
* `IPython.display`
* `OpsUtils` for Tapis interaction (custom module)


##  Usage Example

```python
from OpsUtils import OpsUtils
from MyNotebookTools import interactive_tapis_job_explorer  # or wherever you've defined it

# Connect to Tapis and get job data
t = OpsUtils.connect_tapis()
jobs_df = OpsUtils.get_jobs_dataframe(t)

# Launch explorer
interactive_tapis_job_explorer(t, jobs_df)
```


## Notes

* Designed to be used **inside Jupyter Notebooks**.
* Uses IPython widgets, accordions, and dynamic output panels.
* Handles both full job output sets and individual files.
* Does not require the function to be part of a formal Python package.


#### Files
You can find these files in Community Data.

```{dropdown} interactive_tapis_job_explorer.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/interactive_tapis_job_explorer.py
:language: none
```

