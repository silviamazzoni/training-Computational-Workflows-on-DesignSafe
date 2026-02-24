# find_work_path()
***find_work_path(t, username)***

**This function can take a while and may not be necessary**

This function searches for and returns the **absolute work directory path for a given user** inside the Tapis ***cloud.data* system**, which typically represents shared *Work* storage on DesignSafe.

Because the *Work* system is organized by **group IDs**, and these group folders may be nested under */work* with many thousands of entries, it’s not possible to directly compute the user’s path.

Instead, this function iterates through batches of directories under */work*, looks inside each group folder, and checks if it contains a subfolder named after the specified *username*.
When it finds the match, it returns the Tapis file object containing the user's *workPath*.

---

### How it works, step by step

1. Loops through *offset* pages in chunks of *1000* to handle systems with large numbers of group directories (e.g. */work/05072*, */work/01234*, etc).
2. For each group directory found under */work*:

   * Lists its subfolders.
   * Checks if one of these subfolders matches the *username*.
3. If it finds a folder named exactly like *username*, it:

   * Prints the path,
   * Returns the *hereQ* file object (from which you can get *.path* and other metadata).
4. If it exhausts the offsets or directories, it exits.

---

### Why this is useful

On DesignSafe’s Tapis-backed *cloud.data* (the *Work* system), your actual path might look like:

```
/work/05072/jdoe
```

but the *05072* is a project or allocation group, which your script does not necessarily know ahead of time.
This function **automatically locates your specific work directory**, regardless of which group or allocation ID it is under.

---

### Example usage

```python
work_file_object = find_work_path(t, username='smazzoni')
print('Work path:', work_file_object.path)
```

This lets you build your scripts without hard-coding your group ID.

#### Files
You can find these files in Community Data.

```{dropdown} find_work_path.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/find_work_path.py
:language: none
```


