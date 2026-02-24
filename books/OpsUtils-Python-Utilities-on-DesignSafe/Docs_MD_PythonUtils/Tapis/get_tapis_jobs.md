# get_tapis_jobs()
***get_tapis_jobs(t, SelectCriteria, displayIt=False, NmaxJobs=500)***


This function searches for **Tapis jobs** on a platform like DesignSafe (through the Python Tapis client *t*) based on flexible selection criteria you provide.
It returns:

* a list of matching job UUIDs, and
* a dataframe of all matching job metadata.

It’s designed to support:

* Filtering on **time ranges** or **specific dates** for job lifecycle fields (like *created*, *remoteStarted*, *ended*, *lastUpdated*).
* Filtering on **exact matches** for other metadata fields.

It can also optionally print out the results.

---

### How it works, step by step

1. **Loads job data**

   * Calls your utility *OpsUtils.get_tapis_jobs_df()* to get a dataframe of up to *NmaxJobs* jobs from Tapis, with full metadata.

2. **Loops through your *SelectCriteria* dictionary**, where each key is a field name (like *created*, *status*, *appId*) and the value is:

   * either a list (for ranges or multiple matches), or
   * a single value (for exact matching).

3. **Handles time fields specially:**

   * For *created*, *remoteStarted*, *ended*, or *lastUpdated*:

     * Converts them to **Unix timestamps** using *convert_time_unix*.
     * If you provide a list of two dates, filters between them (inclusive time range).
     * If you provide a single date (YYYY-MM-DD), filters for jobs matching that exact day.

4. **Handles other fields as standard filters:**

   * If you give a list, uses *.isin()* to match any of the values.
   * If you give a single value, matches exactly.

5. **Collects the UUIDs** of matching jobs into *filtered_uuid*.

6. **Optionally displays the UUID list and the filtered dataframe**.

7. **Returns** both:

```python
(filtered_uuid, filtered_df)
```

---

### Example use

```python
SelectCriteria = {
    'created': ['2025-06-01', '2025-06-30'],
    'status': ['FINISHED', 'FAILED'],
    'appId': 'opensees-mp'
}

uuids, df = get_tapis_jobs(t, SelectCriteria, displayIt=True)
```

This would:

* Find all jobs **created in June 2025**,
* with status either **FINISHED or FAILED**,
* and submitted to the **opensees-mp** app.

---

### How it handles dates vs. lists

| Field value type               | Behavior                              |
| ------------------------------ | ------------------------------------- |
| *['2025-06-01', '2025-06-30']* | Filter between two dates (time range) |
| *'2025-06-15'*                 | Exact match on that date              |
| *['FINISHED', 'FAILED']*       | Filter matching any of these statuses |
| *'opensees-mp'*                | Exact match on appId                  |

---

### Why this is powerful

It lets you run **complex, multi-field searches over your Tapis job history** — filtering by date ranges, statuses, app IDs, or any other job metadata in a single call.

This is essential for managing large-scale or repeated computational workflows on platforms like DesignSafe.

---

### How *SelectCriteria* values work

| **Field**                                             | **SelectCriteria value**       | **Behavior**                                   |
| ----------------------------------------------------- | ------------------------------ | ---------------------------------------------- |
| *created*, *remoteStarted*,<br>*ended*, *lastUpdated* | *['YYYY-MM-DD', 'YYYY-MM-DD']* | Filters jobs **between two dates** (inclusive) |
|                                                       | *'YYYY-MM-DD'*                 | Filters jobs **on that exact day**             |
| *status*, *appId*, etc.                               | *['val1', 'val2']*             | Filters jobs matching **any of the values**    |
|                                                       | *'val'*                        | Filters jobs matching **exactly that value**   |

---

### Example call

```python
SelectCriteria = {
    'created': ['2025-06-01', '2025-06-30'],
    'status': ['FINISHED', 'FAILED'],
    'appId': 'opensees-mp'
}

uuids, df = get_tapis_jobs(t, SelectCriteria, displayIt=True)
```

---

### Example snippet of the returned dataframe

| uuid              | name           | status   | created              | appId       | ... |
| ----------------- | -------------- | -------- | -------------------- | ----------- | --- |
| 12ab-34cd-56ef... | job\_case\_001 | FINISHED | 2025-06-15T10:23:45Z | opensees-mp | ... |
| 78gh-90ij-12kl... | job\_case\_002 | FAILED   | 2025-06-20T14:18:02Z | opensees-mp | ... |

---

**In short:**

* Lists: interpreted as **ranges for date fields**, or **multiple options for other fields**.
* Strings: treated as an **exact match**.
  This makes your function extremely flexible for filtering any combination of time and job metadata on Tapis.

#### Files
You can find these files in Community Data.

```{dropdown} get_tapis_jobs.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/get_tapis_jobs.py
:language: none
```

