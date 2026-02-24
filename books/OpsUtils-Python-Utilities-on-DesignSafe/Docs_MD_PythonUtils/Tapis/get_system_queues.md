# get_system_queues()
***get_system_queues(t, system_id="stampede3", display=True)***


This function retrieves and displays the **batch queues available on a given Tapis system** (such as **stampede3** on DesignSafe/TACC).

It does three main things:

1. **Fetches the system definition** from Tapis, including all configured batch queues.
2. **Builds a Pandas DataFrame** summarizing details about each queue (like name, max jobs, max runtime, etc).
3. Optionally **displays the table in a nicely transposed form** (queues as columns, properties as rows) for quick inspection.

It also returns a **Python dictionary keyed by queue name**, so you can easily access the raw queue metadata programmatically.

---

### Why this is useful

* Lets you quickly see all available queues, along with their limits and configurations, right in a notebook.
* Avoids hunting through system documentation.
* Makes it easy to pick the right queue for submitting jobs (for example, deciding based on `maxRequestedTime` or `maxJobs`).

---

#### Files
You can find these files in Community Data.

```{dropdown} get_system_queues.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/get_system_queues.py
:language: none
```

