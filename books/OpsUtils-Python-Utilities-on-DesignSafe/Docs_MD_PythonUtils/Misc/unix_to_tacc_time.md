# unix_to_tacc_time()
***unix_to_tacc_time(unix_time)***

This function converts a **Unix timestamp** (the standard float or integer representing seconds since the Unix **epoch 1970-01-01 00:00:00 UTC**) into a **TACC-style UTC timestamp string**, matching the format typically returned by Tapis or TACC systems.

The output string looks like:

```
"2025-05-07T22:20:52.736325Z"
```

where:

* The **T** separates date and time.
* The fractional seconds provide precise timing.
* The **Z** explicitly marks it as **UTC** (like ISO8601 with **Z**).

It preserves microseconds and explicitly marks the time as UTC with a `Z` suffix.

Use it alongside `convert_tacc_time()` to convert both ways.


###  Why it’s useful

- Logging events in a format consistent with Tapis or TACC jobs.
- Generating timestamps for metadata that need to be uploaded to systems expecting this exact style.
- Round-tripping from Unix time back to the original string format (for example after calculating durations).
* Lets you **format times for logs, reports, or re-upload to systems that expect this exact string format**.
* Keeps all your workflows consistent with how Tapis, TACC, and DesignSafe report timestamps.


#### Files
You can find these files in Community Data.

```{dropdown} unix_to_tacc_time.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Misc/unix_to_tacc_time.py
:language: none
```
