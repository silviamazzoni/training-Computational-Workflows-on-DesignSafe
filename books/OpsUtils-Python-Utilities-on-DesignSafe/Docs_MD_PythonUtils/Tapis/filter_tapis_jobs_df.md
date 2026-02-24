# filter_tapis_jobs_df()
***filter_tapis_jobs_df(SelectCriteria, filtered_df, displayIt=False)***

This function filters a **Tapis jobs DataFrame**, which you typically create with *get_tapis_jobs_df()*, based on flexible user-defined selection criteria provided in a Python dictionary. 

It’s designed to support the various time-related columns typically found in Tapis job metadata, as well as any other column you’d like to filter.

---

### Supported filtering logic
It intelligently handles different types of data:

#### 1. Time-based ranges
For example, if your DataFrame has columns like:
- *created_unix* (seconds since epoch)
- *created_dt* (UTC datetime)
- *created_date* (just date)

and you provide:
```python
SelectCriteria = {'created': ['2024-08-01', '2024-08-31']}
````

the function:

* recognizes *created* is a time field,
* converts your string dates to Unix timestamps,
* and filters *created_unix* to include only jobs submitted in August 2024.

It automatically handles:

* '*_unix' columns: with Unix second comparisons
* '*_dt' columns: with datetime comparisons
* '*_date' columns: with pure date comparisons

#### 2. General *isin* list matching

For non-time columns (like *appId*, *status*), you can pass lists:

```python
SelectCriteria = {'appId': ['opensees-mp-s3', 'opensees-sp-s3']}
```

and it filters rows where **appId** matches any of those values.

#### 3. Single date or exact value matching

For single values (not a list), e.g.:

```python
SelectCriteria = {'created': '2024-08-15'}
```

it checks for jobs submitted exactly on that date.
For other fields (like *status*), it does simple *==* matching.

---

###  How it works internally

1. **Determines the type of filter needed** based on your key and value.
2. If the key is a time column (*created*, *remoteStarted*, *ended*, *lastUpdated*) or any of their suffixes (*_unix*, *_dt*, *_date*), it applies special logic:

   * If you give a range (a list with two values), it does a between-filter.
   * If you give a single date string, it tries to match that date.
3. Otherwise, if you pass a list of values, it applies an `isin` filter.
4. Or if it’s a single value, it does a direct equality check.

---

### Example usage

```python
criteria = {
    'status': ['FINISHED'],
    'appId': ['opensees-mp-s3'],
    'created': ['2024-08-01', '2024-08-31']  # filter by date range
}
uuids, df_filtered = filter_tapis_jobs_df(criteria, JobsData_df, displayIt=True)
```

This will:

* Filter the DataFrame to jobs finished in August 2024, submitted with the *opensees-mp-s3* app.
* Print a summary and show the filtered dataframe.

---

###  Return values

* **filtered\_uuid:** a list of the `uuid` strings for all matching jobs.
* **filtered\_df:** the filtered DataFrame itself.

---

###  Notes & robust design

* The function checks if each key exists in your DataFrame before trying to filter on it, so you can safely pass broad *SelectCriteria*.
* It handles malformed or missing timestamp strings gracefully by converting them to *-1*, which effectively excludes them from time filters.
* The display will show how many jobs matched, their UUIDs (if any), and the top of the filtered DataFrame.

---

### In short:
This is your **central, reusable function for slicing and dicing Tapis job metadata**, making it easy to build interactive dashboards or pipelines that explore your DesignSafe Tapis workflows.


#### Files
You can find these files in Community Data.

```{dropdown} filter_tapis_jobs_df.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/filter_tapis_jobs_df.py
:language: none
```
