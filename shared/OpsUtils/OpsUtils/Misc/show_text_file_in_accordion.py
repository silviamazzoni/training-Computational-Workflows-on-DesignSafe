def show_text_file_in_accordion(folderPathList, filenameList, background='lightyellow', showLineNumbers=True,extraTitleTXT = '',mainAccordionTitle=''):
    """
    Search for specified text files in one or more folders (recursively) and display
    each found file inside a collapsible accordion block in a Jupyter notebook,
    with a copy-to-clipboard button.

    Parameters
    ----------
    folderPathList : str or list of str
        Path(s) to folders to search through (recursively). Accepts a single string 
        or a list of strings. '~' is expanded to the user home.

    filenameList : str or list of str
        Names of files to look for. Accepts a single string or a list of strings.

    background : str, default='#d4fbff'
        Background color for the file content area.

    showLineNumbers : bool, default=False
        If True, prefix each line of the file with a line number (1-based).

    Returns
    -------
    None
        Displays formatted HTML blocks with copy buttons directly in the notebook output.

    Example
    -------
    show_text_file_in_accordion("~/MyProjects/ProjectA", ["slurm.sub", "params.json"],
                                showLineNumbers=True)

    Author
    ------
    Silvia Mazzoni, DesignSafe (silviamazzoni@yahoo.com)

    Date
    ----
    2025-08-14
    2025-12-04

    Version
    -------
    1.2
    """

    from IPython.display import display, HTML,Markdown
    import ipywidgets as widgets
    import os
    import uuid
    from pathlib import Path
    

    if isinstance(folderPathList, str):
        folderPathList = [folderPathList]
    if isinstance(filenameList, str):
        filenameList = [filenameList]

    def _add_line_numbers(text: str) -> str:
        """Prefix each line with a line number."""
        lines = text.splitlines()
        if not lines:
            return text
        width = len(str(len(lines)))  # width of largest line number
        return "\n".join(f"{str(i+1).rjust(width)} | {line}"
                         for i, line in enumerate(lines))


    this_out = widgets.Output()
    if len(mainAccordionTitle)>0: 
        this_accordion = widgets.Accordion(children=[this_out])
        # here_accordion.selected_index = 0
        this_accordion.set_title(0, mainAccordionTitle)
        display(this_accordion)
    else:
        display(this_out)
        
    with this_out:
        for folderPath in folderPathList:
            folderPath = os.path.expanduser(folderPath)
            for root, _, files in os.walk(folderPath):
                for thisFilename in filenameList:
                    if thisFilename in files:
                        filepath = os.path.join(root, thisFilename)
                        accordionTitle = f'{thisFilename} {extraTitleTXT}'
                        path = Path(filepath)
                        unique_id = uuid.uuid4().hex  # unique id for each block to attach copy
                        doHTML = True
                        copyButtonHTML = f"""<button onclick="navigator.clipboard.writeText(document.getElementById('{unique_id}').innerText)">📋 Copy</button>"""                    
                        try:
                            with open(filepath, "r", encoding="utf-8") as file:
                                content = file.read()
                            if showLineNumbers:
                                content_to_show = _add_line_numbers(content)
                            else:
                                if path.suffix.lower() == '.md':
                                    # content_to_show = Markdown(content)
                                    here_out = widgets.Output()
                                    here_accordion = widgets.Accordion(children=[here_out])
                                    # here_accordion.selected_index = 0
                                    here_accordion.set_title(0, accordionTitle)
                                    display(here_accordion)
                                    # content = Markdown(content)
                                    content = f'<div id="{unique_id}" style="background-color:white;border:20px {background} solid;padding:20px;"><b>{filepath}</b><br> {content}</div>'
                                    with here_out:
                                        # display(HTML(f'<div style="background-color: {background};border:20px blue solid;"><b># {filepath}</b></div>'))
                                        display(HTML(copyButtonHTML))
                                        display(Markdown(content))
                                        # display(Markdown(content))
                                    continue
                                else:
                                    content_to_show = content
                                    copyButtonHTML = ""
    
    
                        
                        except Exception:
                            # continue
                            content_to_show = 'CANNOT Display File Content'
                            copyButtonHTML = ""
    
                     
    
                        html = f"""
                          <details style="margin-top:1em; font-family:monospace; background:white; 
                              padding:0.25em; border-radius:6px; border:1px solid #ccc;">
                            <summary style="cursor:pointer; font-weight:bold; background:white; 
                              padding:0.3em 0.5em; border-radius:4px;">{accordionTitle}</summary>
                            {copyButtonHTML}
                            <pre id="{unique_id}" style="white-space:pre-wrap; margin:0.25em 0 0 0; 
                                background:{background}; padding:2.3em; border-radius:5px;"><b>{filepath}</b>\n{content_to_show}</pre>
                          </details>
                        """
                        display(HTML(html))
