def display_content_in_accordion(content,accordionTitle='...more'):
    from IPython.display import display, HTML,Markdown
    import ipywidgets as widgets
    here_out = widgets.Output()
    here_accordion = widgets.Accordion(children=[here_out])
    # here_accordion.selected_index = 0
    here_accordion.set_title(0, accordionTitle)
    display(here_accordion)
    with here_out:
        display(content)
