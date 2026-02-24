# convert_tacc_time()
***convert_tacc_time(timestamp_str)***

This function converts a **TACC-style timestamp string** (typical of Tapis job metadata and DesignSafe logs) into a **Unix timestamp** (seconds since epoch).

It expects a timestamp in the format:

```
"YYYY-MM-DDTHH:MM:SS.ssssssZ"
```

where the **Z** at the end indicates it’s in UTC.

This is essential for comparing times numerically, doing duration calculations, or sorting by time.

---

### Typical use case

For example, given:

```python
"2025-05-07T22:20:52.736325Z"
```

it will produce:

```
1751884852.736325
```

which is the number of seconds since 1970-01-01 UTC.



#### Files
You can find these files in Community Data.

```{dropdown} convert_tacc_time.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Misc/convert_tacc_time.py
:language: none
```
