# analyze_tacc_job_history()
***analyze_tacc_job_history(t, jobUuid, mode="summary")***

This is a **Python utility function** designed to simplify inspecting or extracting information from a TACC (Texas Advanced Computing Center) job’s execution history. It’s a wrapper around another function *process_tacc_job_history*, adding convenience “modes” so you don’t have to set many arguments manually.


* It takes in:

  * *t* : likely a Tapis or TACC client object used to communicate with the job system.
  * *jobUuid* : the unique ID of the job whose history you want to analyze.
  * *mode* : a string that controls **how much information is displayed or returned**.

* Based on the *mode* you pick, it calls *process_tacc_job_history* with different options, so you can easily:

  * **See a quick summary** of the job history.
  * **Print the full details**, very verbose (all steps, all times, all inputs).
  * **Just get structured data** back, without printing anything.

---

### Modes

| Mode        | What it does                                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| *"summary"* | Prints key stages of the job, how long each stage took, and relevant input info.                                                      |
| *"full"*    | Prints all available details about the job’s lifecycle (like *printAllAll=True*).                                                     |
| *"data"*    | Returns the structured data (probably a dict or list of records) without printing anything, so you can process or visualize it later. |

If you pass an invalid mode, it prints an error message telling you to use *"summary"*, *"full"*, or *"data"*.

---

### Quick summary

This function lets you easily analyze a job’s lifecycle on TACC by picking how much information you want:

* Use *"summary"* for a concise report,
* *"full"* for a very detailed step-by-step log,
* or *"data"* to get raw structured data for plotting or saving.

It makes interacting with *process_tacc_job_history* simpler by hiding repetitive parameter choices under named modes.

### Example usage

***python
# Quick human-readable summary
analyze_tacc_job_history(t, jobUuid, mode="summary")

# Full debug dump
analyze_tacc_job_history(t, jobUuid, mode="full")

# Structured data for plotting / logs
job_data = analyze_tacc_job_history(t, jobUuid, mode="data")
***

With this wrapper function you can reuse your powerful underlying *process_tacc_job_history* exactly as before — but with a simpler interface for common workflows.


#### Files
You can find these files in Community Data.

```{dropdown} analyze_tacc_job_history.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/analyze_tacc_job_history.py
:language: none
```
