# get_now_unix()
***get_now_unix()***

This is a simple utility function that returns the **current time as a Unix timestamp**, in **UTC**.

That means it gives you:

* the number of **seconds since the Unix epoch** (1970-01-01 00:00:00 UTC),
* as a floating point number (includes fractions of a second).


### How it works

1. **Imports *datetime* and *timezone*** from Python’s standard library.

2. Uses:

```python
datetime.now(timezone.utc)
```

to get the current time **explicitly in UTC**.

3. Calls *.timestamp()* on that *datetime* object, which converts it to a Unix timestamp (a float).

4. Returns that value.


### Example usage

```python
now_unix = get_now_unix()
print(now_unix)
# → 1751234567.890123
```

### Why explicitly UTC?

Without specifying *timezone.utc*, *datetime.now()* would return **local time**, which might vary based on your server or laptop’s timezone.
By doing *datetime.now(timezone.utc)*, this function ensures it **always returns UTC**, which is critical for consistent comparisons in workflows like Tapis job metadata.


### Typical use cases

* Comparing against job times (like *created_unix* or *ended_unix* fields).
* Logging events in a consistent UTC format.
* Calculating durations by subtracting from other Unix timestamps.


### In short
*get_now_unix()* gives you the **current moment in UTC**, expressed in seconds since epoch — a lightweight, always-consistent time format ideal for automation and data tracking.



#### Files
You can find these files in Community Data.

```{dropdown} get_now_unix.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Misc/get_now_unix.py
:language: none
```
