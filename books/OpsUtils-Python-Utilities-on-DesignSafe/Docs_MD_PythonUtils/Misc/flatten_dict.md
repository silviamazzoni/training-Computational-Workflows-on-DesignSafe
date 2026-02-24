# flatten_dict()

***flatten_dict(d, parent_key='', sep='.')***

This is a **powerful recursive utility** that takes a deeply nested data structure — such as JSON responses, Tapis job objects, or multi-level Python dictionaries — and flattens it into a **single-level dictionary** with compound keys.

It handles:

* **Nested dictionaries**, joining keys with a separator (like **.**).
* **Lists**, using index notation (e.g. **key[0]**, **key[1]**).
* **TapisResult objects**, by flattening their internal attributes.
* **JSON strings that are themselves dictionaries**, parsing them and continuing to flatten.
* Leaves simple values (`None`, strings, numbers, booleans) unchanged.

This is especially useful for:

* Preparing complex API responses for DataFrame creation or CSV export.
* Searching or filtering on nested keys.
* Logging structured data in a flat, human-readable form.

---

### Example input vs. output

```python
nested_test = {
    "job": {
        "id": "123",
        "status": "RUNNING",
        "details": {"queue": "normal", "nodes": 2},
        "history": [
            {"time": "2025-06-30T12:00:00Z", "event": "QUEUED"},
            {"time": "2025-06-30T12:10:00Z", "event": "RUNNING"}
        ]
    },
    "owner": "smazzoni"
}

flattened_test = OpsUtils.flatten_dict(nested_test)

print(flattened_test)
```

Produces:

```python
{
    'job.id': '123',
    'job.status': 'RUNNING',
    'job.details.queue': 'normal',
    'job.details.nodes': 2,
    'job.history[0].time': '2025-06-30T12:00:00Z',
    'job.history[0].event': 'QUEUED',
    'job.history[1].time': '2025-06-30T12:10:00Z',
    'job.history[1].event': 'RUNNING',
    'owner': 'smazzoni'
}
```

Or you can request each key:

```python
print("Flattened dictionary keys:")
for key in flattened_test:
    print(f" - {key}: {flattened_test[key]}")
```

Produces:

```python
Flattened dictionary keys:
 - job.id: 123
 - job.status: RUNNING
 - job.details.queue: normal
 - job.details.nodes: 2
 - job.history[0].time: 2025-06-30T12:00:00Z
 - job.history[0].event: QUEUED
 - job.history[1].time: 2025-06-30T12:10:00Z
 - job.history[1].event: RUNNING
 - owner: smazzoni
```

---

#### Files

You can find these files in **Community Data**.

````{dropdown} flatten_dict.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Misc/flatten_dict.py
:language: none
````
