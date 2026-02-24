# show_video()
***show_video(videoPath, width="75%", videoType="video/mp4")***

This function displays a video file **directly inside a Jupyter notebook** using a clean, styled HTML **<video>** tag.
It lets you specify:

* The **file path** to your video,
* The **display width** (with responsive auto height),
* The **MIME type** (like *video/mp4*).

It also adds a border, rounded corners, and a subtle drop shadow for a polished look.

This is perfect for:

* Showing animations of structural models, finite element analyses, or simulation results.
* Demonstrating time-lapse experiments or visualization outputs.
* Embedding any local or served video file in your notebooks.

---

### Typical use

```python
show_video("results/animation.mp4", width="50%")
```

This will embed the video at half the width of your notebook cell.


#### Files
You can find these files in Community Data.

```{dropdown} show_video.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Misc/show_video.py
:language: none
```
