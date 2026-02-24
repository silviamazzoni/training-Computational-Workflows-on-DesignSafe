def display_images_in_xbox(image_paths, box_type='V', width="100%", format='jpg'):
    """
    Display a list of images in a bordered, scrollable container in a Jupyter notebook.

    Each image is wrapped with a border, margin, and padding for a clean layout.
    You can choose to display the images stacked vertically (VBox) or side-by-side 
    horizontally (HBox), with automatic scrolling if there are many.

    Parameters
    ----------
    image_paths : list of str
        List of paths to image files to display.

    box_type : str, default='V'
        'V' for vertical stacking (VBox), anything else for horizontal (HBox).

    width : str, default='100%'
        The CSS width for each image (use '300px', '100%', etc).

    format : str, default='jpg'
        The image format, passed to ipywidgets Image.

    Returns
    -------
    None
        Displays the scrollable image box in the notebook.

    Example
    -------
    display_images_in_xbox(['fig1.jpg', 'fig2.jpg', 'fig3.jpg'], box_type='H', width='300px')

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

    from IPython.display import display
    import ipywidgets as widgets
    from PIL import Image
    import os
    # Create styled image widgets with borders
    image_widgets = []
    for path in image_paths:
        if os.path.exists(path):
            with open(path, 'rb') as file:
                img_data = file.read()
                img_widget = widgets.Image(value=img_data, format=format, width=width)
    
                # Wrap the image in a box with a border
                bordered = widgets.Box([img_widget], layout=widgets.Layout(
                    border='2px solid black',
                    padding='5px',
                    margin='5px'
                ))
                image_widgets.append(bordered)
        else:
            print(f"⚠️ File not found: {path}")
    
    # Display images in a scrollable horizontal box
    if box_type=='V':
        scroll_box = widgets.VBox(image_widgets, layout=widgets.Layout(overflow_x='auto'))
    else:
        scroll_box = widgets.HBox(image_widgets, layout=widgets.Layout(overflow_x='auto'))
    display(scroll_box)