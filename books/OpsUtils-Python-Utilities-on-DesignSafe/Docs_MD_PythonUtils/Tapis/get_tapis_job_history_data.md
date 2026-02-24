# get_tapis_job_history_data()

***get_tapis_job_history_data(t, jobUuid, print_out=True, return_data=False, get_job_error_message=False)***

Analyze and summarize a Tapis job’s **full history**: compute **time-in-status** (e.g., QUEUED, RUNNING), extract **input/archive transfer** metrics and durations, and capture any **JOB_ERROR_MESSAGE** entries. Prints a clean, sectioned summary (Jupyter‑friendly) and can **return structured data** for plotting or logs.

## What it does

* Fetches *jobs.getJobHistory(...)*.
* Aggregates **status durations** and total time.
* Parses **transferSummary** for input/archive staging events.
* Collects and prints **job error messages** (if present).
* Prints via **ipywidgets Accordions** when available; otherwise falls back to plain text.

## Parameters

* *t* *(tapipy.tapis.Tapis)* — Authenticated Tapis client.
* *jobUuid* *(str)* — UUID of the target job.
* *print_out* *(bool, default *True*)* — Print the summary sections.
* *return_data* *(bool, default *False*)* — Return structured data dictionaries.
* *get_job_error_message* *(bool, default *False*)* — Ensure error section prints when errors exist.

## Returns

When **return_data=True**, a dictionary:

```python
{
  "StepsMetricsDict": {            # status durations and created timestamps
      "created": {status: iso_str, ...},
      "duration": {status: seconds, ..., "TOTAL": seconds}
  },
  "DataTransfersDict": {           # per transfer event (input/archive)
      "JOB_INPUT_TRANSACTION_ID": {
          "estimatedTotalBytes": ...,
          "totalBytesTransferred": ...,
          "completeTransfers": ...,
          "totalTransfers": ...,
          "Create-to-TransferStart Duration": ...,
          "TransferStart-to-TransferEnd Duration": ...,
          "Create-to-TransferEnd Duration": ...
      },
      "JOB_ARCHIVE_TRANSACTION_ID": { ... }
  },
  "JobHistory": [...],             # original entries from Tapis
  "JobErrorList": [                # captured JOB_ERROR_MESSAGE entries
      {"event": "...", "created": "...", "eventDetail": "...",
       "jobStatus": "...", "message": "..."},
      ...
  ]
}
```

Otherwise returns **None**. On API failure, returns **-1**.

## Example

```python
# Print sections and capture structured data for charts
summary = get_tapis_job_history_data(t, jobUuid, print_out=True, return_data=True)

# Example: get total runtime and bytes transferred
total_runtime = summary["StepsMetricsDict"]["duration"].get("TOTAL", 0)
input_stats = summary["DataTransfersDict"].get("JOB_INPUT_TRANSACTION_ID", {})
bytes_moved = input_stats.get("totalBytesTransferred", 0)
print(total_runtime, bytes_moved)
```

## Notes

* Timestamps are treated as **UTC**; function accepts both *...Z* and ISO with offset.
* If a job is still **RUNNING/QUEUED**, the **last segment is open**, so the **TOTAL** reflects only completed segments.
* Works in notebooks *and* terminals (widgets are optional).


---

#### Files
You can find these files in Community Data.

```{dropdown} get_tapis_job_history_data.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/get_tapis_job_history_data.py
:language: none
```


