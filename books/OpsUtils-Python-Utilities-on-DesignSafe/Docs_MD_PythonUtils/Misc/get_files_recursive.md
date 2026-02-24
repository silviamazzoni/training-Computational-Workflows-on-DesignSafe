# get_files_recursive()

**Signature:** `get_files_recursive(path="", displayIt=10, returnItems=False, displayLevel=0)`

A small, reliable helper that **recursively lists files** under a directory, optionally **prints** a concise view (files before directories), and can **return** a structured dictionary containing counts and paths.

## What it does

* Walks the tree rooted at *path* (or *"."* if empty).
* **Displays** up to *displayIt* files per directory level when *displayIt* is an integer ≥ 2.
* **Displays everything** when *displayIt=True* and **nothing** when *False*.
* Always lists **files before directories** at each level.
* Skips *.ipynb_checkpoints*.

## Parameters

* *path* *(str, default "")*: Root directory to traverse. Empty string means current working directory.
* *displayIt* *(bool | int, default 10)*:

  * *True* → print all files
  * *False* → print nothing
  * *int >= 2* → print up to that many files per directory level and show a suppression note after the limit
  * *0 or 1* → treated as “no limit” (prints everything when display is on)
* *returnItems* *(bool, default False)*: If *True*, return a dictionary with counts and path lists.
* *displayLevel* *(int, default 0)*: Internal recursion depth; leave as default when calling.

## Returns (when `returnItems=True`)

```python
{
  'Nfiles': <int>,          # total number of files found
  'LocalPath': [..],        # file paths relative to `path` (or "." if empty)
  'FullPath':  [..],        # absolute file paths
  'Items':     [..],        # basenames of files
}
```

## Examples

### 1) Print up to 10 files per directory and capture results

```python
results = get_files_recursive("data", displayIt=10, returnItems=True)
print("Total files:", results['Nfiles'])
```

### 2) Quietly traverse and just get the paths

```python
results = get_files_recursive("data", displayIt=False, returnItems=True)
print(results['FullPath'][:5])  # peek at the first five absolute paths
```

### 3) Print everything (no suppression)

```python
get_files_recursive("data", displayIt=True, returnItems=False)
```

## Notes

* Errors like **not found** or **permission denied** are reported (at the top-level display) and produce an empty result if `returnItems=True`.
* `LocalPath` preserves the relative structure rooted at *path*, while *FullPath* gives absolute paths for convenience.

---

#### Files
You can find these files in Community Data.

```{dropdown} get_files_recursive.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Misc/get_files_recursive.py
:language: none
```
