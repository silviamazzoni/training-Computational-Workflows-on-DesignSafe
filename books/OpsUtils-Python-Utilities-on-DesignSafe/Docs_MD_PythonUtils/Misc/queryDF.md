# queryDF()
***queryDF(outKey, JobsData_df, key, values, displayIt=False)***

This function provides a **simple way to query a Pandas DataFrame for rows matching a set of values**, then returns the corresponding values from another column (keyed by `outKey`).

In other words, it’s a flexible **filter + select utility**, designed for quickly extracting specific metadata (like a UUID) based on other column values (like an index or status).

It also includes:

* Checks to ensure your column names are valid.
* Automatic wrapping of **values** into a list if you pass a single value.
* A compact optional display printout for quick interactive exploration.



###  Typical use

This is especially helpful with Tapis job metadata DataFrames, for quickly extracting things like:

* The **uuid** of a job by filtering on **index_column**
* The **status** of a job by filtering on **appId**



###  Example

```python
uuid_result = queryDF(**uuid**, filtered_df, **index_column**, 388, True)
```

This will:

* Filter **filtered_df** where *index_column == 388*
* Return the corresponding **uuid**
* Print the found mapping if *displayIt=True*.


###  Example DataFrame 
The Dataframe could be a slice of your Tapis jobs dataframe:

```
import pandas as pd

data = {
    'index_column': [101, 102, 103, 104],
    'uuid': ['abc-1', 'def-2', 'ghi-3', 'jkl-4'],
    'status': ['FINISHED', 'FAILED', 'FINISHED', 'QUEUED']
}
df = pd.DataFrame(data)

# Example 1: Single value match
uuid_result = OpsUtils.queryDF('uuid', df, 'index_column', 103, displayIt=True)

# Example 2: Multiple value match
uuids_for_status = OpsUtils.queryDF('uuid', df, 'status', ['FINISHED', 'QUEUED'], displayIt=True)
```

Produces:
```
outKey=ghi-3  for index_column=[103]
outKey=['abc-1', 'ghi-3', 'jkl-4']  for status=['FINISHED', 'QUEUED']
```

#### Files
You can find these files in Community Data.

```{dropdown} queryDF.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Misc/queryDF.py
:language: none
```
