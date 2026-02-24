def show_video(videoPath, width="100%", videoType="video/mp4"):
    """
    Display a video file in a Jupyter notebook with styled HTML.

    This function embeds a video using an HTML <video> tag, adds 
    borders, rounded corners, and a drop shadow for clean presentation.

    Parameters
    ----------
    videoPath : str
        Path to the video file (local or relative to the notebook).

    width : str, default="75%"
        CSS width to display the video. Height is set to auto.

    videoType : str, default="video/mp4"
        MIME type of the video. Use "video/webm", etc. if needed.

    Returns
    -------
    None
        Displays the video directly in the notebook cell.

    Example
    -------
    show_video("results/animation.mp4", width="50%")

    Author
    ------
    Silvia Mazzoni, DesignSafe (silviamazzoni@yahoo.com)

    Date
    ----
    2025-08-14

    Version
    -------
    1.0
    """

    from IPython.display import HTML
    html = f"""
    <video controls style="width: {width}; height: auto; display: block; margin: 20px; 
        border: 3px solid black; border-radius: 6px; box-shadow: 5px 5px 15px rgba(0,0,0,0.5);">
      <source src="{videoPath}" type="{videoType}">
      Your browser does not support the video tag.
    </video>
    """
    display(HTML(html))

    