# get_tapis_jobs_df()
***get_tapis_jobs_df(t, displayIt=False, NmaxJobs=500)***


This function retrieves your jobs from Tapis using the standard **Tapis utility `getJobList()`**, then converts them into a **pandas DataFrame** for easy exploration and filtering.

It provides a **tabular, familiar way to inspect your Tapis job metadata**, whether you want to quickly list all jobs, filter by app, status, or date, or prepare data for more advanced analysis.

---

#### How it works step by step

##### 1. Retrieves jobs using `getJobList()`

```python
jobslist = t.jobs.getJobList(limit=NmaxJobs)
```

* **getJobList()** is a core Tapis utility that fetches job metadata.
* It pulls high-level info about **all your jobs**, whether they were submitted via the Tapis API or through web portals (like OpenSeesMP on DesignSafe).
* This is typically your **first step** in exploring job data.

* We intentionally **do not** use search criteria on *getJobList*, because in practice they can be unreliable.
Instead, we fetch everything and filter later in pandas.

##### 2. Converts TapisResult objects to dictionaries

```python
jobsdicts = [job.__dict__ for job in jobslist]
```

* Each returned item is a *TapisResult* — a custom Python object.
* Calling *. __dict__* extracts its internal fields into a plain Python dictionary, making it easy to work with pandas.


##### 3. Builds a pandas DataFrame

```python
import pandas as pd
df = pd.DataFrame(jobsdicts)
```

* Turns your list of plain dictionaries into a rich, tabular dataframe.

##### 4. Adds a numeric index column

```python
df["index_column"] = df.index
```

* Useful for quickly referencing rows.

##### 5. Reorders columns for convenience

```python
startCols = ['index_column', 'name', 'uuid', 'status', 'appId', 'appVersion']
```

* Puts the most important metadata up front — if those columns exist.
* Uses a safe check (`existingStartCols`) so it doesn’t break if any are missing.

##### 6. Optionally displays results

* Controlled by the *displayIt* argument:

  * *True* or *'displayAll'* shows the entire dataframe.
  * *'head'* or *'displayHead'* shows just the first few rows.

##### 7. Returns the dataframe

So you can filter it, search by app, group by date, or pass it to another function (like your `get_tapis_job`).

---

#### Why this is useful

* This function gives you a **fast, robust way to pull your entire Tapis job history** into a familiar pandas DataFrame.

* It’s the foundation for:

* Finding jobs by status, app, or submission window.
* Generating summary tables.
* Preparing lists of job UUIDs to drill down with functions like *getJob*, *getJobOutputList*, or *getJobOutputDownload*.

---

#### Example usage

```python
df = get_tapis_jobs_df(t, displayIt='head', NmaxJobs=1000)
```

Prints the top of the dataframe so you can quickly see your recent jobs.

---

###  Notes on **getJobList()** vs direct search

* *getJobList()* is the **standard Tapis method** to list jobs.
* It pulls high-level metadata on **all jobs**, including:

  * *uuid*, *name*, *status*, *created*, *appId*, and more.
* We avoid filtering in the API call itself and instead rely on pandas for local, flexible, reliable filtering.

---

##  In short

**get_tapis_jobs_df** uses Tapis **getJobList()** to fetch all your jobs, converts them to a pandas DataFrame, puts the most important columns up front, and lets you immediately explore or process your job history.

---

### Example process in Python:

```python
# pull jobs
jobslist = t.jobs.getJobList(limit=500)
# convert to dicts
jobsdicts = [job.__dict__ for job in jobslist]
# build dataframe
import pandas as pd
df = pd.DataFrame(jobsdicts)
# reorder columns, add index
df["index_column"] = df.index
```

This gives you a **powerful local snapshot of your jobs**, ready for filtering, querying, or driving downstream workflows.



#### Files
You can find these files in Community Data.

```{dropdown} get_tapis_jobs_df.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/get_tapis_jobs_df.py
:language: none
```

