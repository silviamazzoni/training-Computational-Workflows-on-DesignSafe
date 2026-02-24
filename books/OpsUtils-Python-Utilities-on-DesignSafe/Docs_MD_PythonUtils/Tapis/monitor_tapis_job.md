# monitor_tapis_job()
***monitor_tapis_job(t,jobUuid,job_start_time,askConfirmMonitorRT = True)***

Continuously monitors the status of a Tapis job in **real-time**, polling the job status at progressively increasing intervals and printing structured updates.
It provides immediate feedback on status changes, reports how long each state lasted, and stops once the job finishes, fails, or exceeds a maximum monitoring duration.

**Inputs:**

* **t** (*Tapis client object*):
  Authenticated Tapis client instance (e.g. from *tapis3* or *py-tapis*), used to query job status.
* **jobUuid** (*str*):
  UUID of the job to monitor.
* **job_start_time** (*float*):
  The start time of the job in epoch seconds (usually *time.time()* from when the job was submitted).
* **askConfirmMonitorRT** (*bool*, optional):
  If *True* (default), prompts the user for confirmation to begin real-time monitoring.
  If *False*, immediately starts monitoring without asking.

**Outputs:**

* Prints elapsed time and current job status in structured updates until the job completes (or fails, stops, or times out).
* Does **not return a value**; side-effect is printed console output.

**Behavior:**

* Polls job status repeatedly, printing:

  ```
  Elapsed job time: X sec    Current Status: <status>   (previous <status> took Y sec)
  ```
* Waits slightly longer over time (increasing polling interval) to reduce server load.
* Stops if the total monitoring time exceeds **1 hour** (or \~3600 seconds) or after **too many consecutive failures to contact the API**.

**Example usage:**

```python
monitor_tapis_job(t, jobUuid, time.time())
# If askConfirmMonitorRT=False, starts without asking:
monitor_tapis_job(t, jobUuid, time.time(), askConfirmMonitorRT=False)
```

---

#### Files
You can find these files in Community Data.

```{dropdown} monitor_tapis_job.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/monitor_tapis_job.py
:language: none
```

