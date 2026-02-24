# show_text_file_in_accordion()
***show_text_file_in_accordion(folderPathList, filenameList, background='#d4fbff')***

This function searches through one or more folders (including subfolders) for specified text files, and displays each found file **inside a collapsible accordion-style block** in a Jupyter notebook.

Each block shows:

* The full path of the file at the top.
* The contents of the file in a styled *pre* tag for easy reading.

This is perfect for:

* Displaying input scripts, job logs, or metadata files right inside your notebook.
* Keeping the output clean and organized with expandable sections.

It also highlights the background with a customizable color (default is a light blue).


### Typical use cases

* Reviewing multiple job submission files (e.g. *slurm.sub*) in a training notebook.
* Displaying example input files (like *OpenSees.tcl* or *params.json*) from multiple directories.
* Debugging by quickly opening several *stdout.txt* or *stderr.txt* files.


#### Files
You can find these files in Community Data.

```{dropdown} show_text_file_in_accordion.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Misc/show_text_file_in_accordion.py
:language: none
```
