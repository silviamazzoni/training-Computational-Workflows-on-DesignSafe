# convert_time_unix()
***convert_time_unix(timestamp_str)***


This is a useful function to convert formatted date/time from tacc or user input into unix time. This needs to be done when comparing dates/times

This function converts a **timestamp string** (in various common ISO 8601 formats) into a **Unix time (seconds since epoch, UTC)**.
It can handle timestamps with or without fractional seconds and with or without a trailing **Z** for UTC.

If the input is invalid or empty, it returns **-1**.

####  How it works

1. **Imports needed modules:**

   * *datetime* and *timezone* from the standard library to parse and set UTC.
   * *re* to detect fractional seconds.

2. **Handles edge cases:**

   * If *timestamp_str* is *None* or empty, it returns *-1*.

3. **Detects if UTC is specified:**

   * Checks if the string ends with *'Z'* (common in ISO UTC timestamps like *2025-06-30T18:04:02Z*).
   * Removes the *'Z'* for parsing.

4. **Determines the format:**

   * If it has a *T*, it treats it as a datetime.
   * Uses regex to see if fractional seconds (like *.123456*) are present.
   * Falls back to just a date (*%Y-%m-%d*) if *T* isn’t present.

5. **Parses the string into a *datetime* object** using *strptime*.

6. **Sets timezone to UTC** explicitly (regardless of input).

7. **Converts to Unix time** (seconds since 1970-01-01 UTC) using *timestamp()*.

8. **Handles any exceptions:**

   * If parsing fails, it prints an error message and returns *-1*.

---

####  Examples

```python
convert_time_unix('2025-06-30T18:04:02Z')
# → 1751222642.0

convert_time_unix('2025-06-30T18:04:02.123456Z')
# → 1751222642.123456

convert_time_unix('2025-06-30')
# → 1751174400.0

convert_time_unix('bad-date')
# Prints error, returns -1
```

---

####  Summary

| Input example                   | Format detected              | Output (UTC Unix time) |
| ------------------------------- | ---------------------------- | ---------------------- |
| *'2025-06-30T18:04:02Z'*        | *%Y-%m-%dT%H:%M:%S*          | *1751222642.0*         |
| *'2025-06-30T18:04:02.123456Z'* | *%Y-%m-%dT%H:%M:%S.%f*       | *1751222642.123456*    |
| *'2025-06-30'*                  | *%Y-%m-%d*                   | *1751174400.0*         |
| *None* or *''*                  | (caught early)               | *-1*                   |
| Bad format (e.g. *'abc'*)       | (prints error, returns *-1*) | *-1*                   |



#### Files
You can find these files in Community Data.

```{dropdown} convert_time_unix.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Misc/convert_time_unix.py
:language: none
```
