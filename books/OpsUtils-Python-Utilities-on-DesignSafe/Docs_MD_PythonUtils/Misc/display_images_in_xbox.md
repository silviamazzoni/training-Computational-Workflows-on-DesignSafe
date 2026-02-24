# display_images_in_xbox()
***display_images_in_xbox(image_paths, box_type='V', width="100%", format='jpg')***


This function displays a list of image files **inside a visually styled scrollable box** (either horizontally or vertically) directly in a Jupyter notebook.

### How it works

* Reads each image from the provided paths.
* Wraps it in a small bordered box with padding and margin for a neat appearance.
* Collects all these boxes into either a *VBox* (vertical stack) or *HBox* (horizontal row) from *ipywidgets*.
* Prints a warning if any file does not exist.
* Finally, it displays the entire scrollable set of images in the notebook.

This is perfect for comparing multiple figures, slides, or plots in a clean, organized way inside your Jupyter environment.


###  Typical uses

* Reviewing a series of OpenSees plots or results.
* Browsing through image files from a simulation or experiment.
* Comparing before/after images side by side.

#### Files
You can find these files in Community Data.

```{dropdown} display_images_in_xbox.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Misc/display_images_in_xbox.py
:language: none
```
