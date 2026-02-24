# empty_folder()
***empty_folder(folder_path,delete_folder=False,confirm=True) -> str***


The *empty_folder* function is a convenient utility to help manage local directories.
It can:

* **Empty all contents inside a folder** (files, subfolders, symlinks),
* Or **optionally delete the folder itself**,
* With a confirmation prompt to prevent accidental deletions.

It uses modern *pathlib* for paths and *shutil.rmtree* for recursive folder cleanup.


## Function signature

```python
empty_folder(
    folder_path,
    delete_folder=False,
    confirm=True
) -> str
```


## Parameters

| Parameter       | Type             | Description                                                                                                                 |
| --------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------- |
| *folder_path*   | *str* or *Path*  | Path to the target folder to clear or delete.                                                                               |
| *delete_folder* | *bool*, optional | If *True*, deletes the folder itself after clearing its contents. Default is *False* (only empties contents, keeps folder). |
| *confirm*       | *bool*, optional | If *True* (default), prompts for a manual confirmation (*yes*) before proceeding. Helps avoid accidental deletions.         |


## Returns

Returns a *str* indicating what was done:

| Return value         | Meaning                                                           |
| -------------------- | ----------------------------------------------------------------- |
| *'deleted'*          | Folder and all contents were deleted.                             |
| *'emptied'*          | Contents of the folder were cleared, but the folder still exists. |
| *'folder not found'* | The specified folder path does not exist.                         |
| *'cancelled'*        | The user chose not to proceed at the confirmation prompt.         |
| *'error'*            | An unexpected exception occurred during deletion.                 |


## Example usage

### Empty the contents of a folder (keeping the folder)

```python
empty_folder("results/")
```


### Delete the entire folder and its contents

```python
empty_folder("old_simulations/", delete_folder=True)
```


### Prompt user before deleting

```python
empty_folder("outputs/", delete_folder=True, confirm=True)
# Will display:
# Do you want to clear the contents of
#   "outputs"? (and delete the folder itself) (yes/no/stop):
```

### Skip confirmation

```python
empty_folder("logs/", confirm=False)
```


## Behavior summary

| *delete_folder* | *confirm* | What happens                                                     |
| --------------- | --------- | ---------------------------------------------------------------- |
| *False*         | *True*    | Asks before **emptying contents**, keeps folder.                 |
| *True*          | *True*    | Asks before **deleting folder and all contents**.                |
| *True*          | *False*   | Deletes folder + contents **immediately**, without confirmation. |
| *False*         | *False*   | Clears contents **immediately**, without confirmation.           |


## Safety notes

* This function uses *shutil.rmtree* and *Path.unlink*, which perform **permanent deletion**.
  Files and subfolders are not moved to trash/recycle bin.
* Always test on a sample folder first if unsure.


#### Files
You can find these files in Community Data.

```{dropdown} empty_folder.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Misc/empty_folder.py
:language: none
```
