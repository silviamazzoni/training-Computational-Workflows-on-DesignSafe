def view_tapis_file_in_accordion(t,jobUuid,selected_path, showLineNumbers=False):
   
    import ipywidgets as widgets
    from IPython.display import display, clear_output
    from html import escape
    
    # thresholds you can tune
    TEXTAREA_CHAR_LIMIT = 200_000     # ~200 KB of text
    TEXTAREA_MAX_LINE   = 2_000       # lines wider than this favor <pre>
    
    def _bytes_to_text(data: bytes, path: str = "") -> str | None:
        """Return decoded text, or None if this looks binary."""
        if not isinstance(data, (bytes, bytearray)):
            return str(data)
        lower = path.lower()
        if lower.endswith((
            ".zip",".gz",".bz2",".xz",".tgz",".tar",
            ".png",".jpg",".jpeg",".gif",".pdf",".h5",".npy",".npz",
            ".so",".exe",".xlsx",".pptx",".docx"
        )):
            return None
        if b"\x00" in data:
            return None
        for enc in ("utf-8", "utf-16", "latin-1"):
            try:
                return data.decode(enc)
            except UnicodeDecodeError:
                pass
        return data.decode("utf-8", errors="replace")
    
    def _should_use_pre(text: str, nbytes: int) -> bool:
        """Heuristic chooser: True => HTML <pre>, False => Textarea."""
        if nbytes > TEXTAREA_CHAR_LIMIT:
            return True
        if len(text) > TEXTAREA_CHAR_LIMIT:
            return True
        # Check longest line (cap sample to avoid O(N) on huge files)
        it = iter(text.splitlines())
        longest = 0
        for _ in range(50_000):  # sample first 50k lines max
            try:
                ln = next(it)
            except StopIteration:
                break
            if len(ln) > longest:
                longest = len(ln)
                if longest > TEXTAREA_MAX_LINE:
                    return True
        return False

    def _add_line_numbers(text: str) -> str:
        """Optionally prefix each line with a line number."""
        lines = text.splitlines()
        if not lines:
            return text
        width = len(str(len(lines)))  # width of the largest line number
        return "\n".join(f"{str(i+1).rjust(width)} | {line}"
                         for i, line in enumerate(lines))

    view_select_out = widgets.Output()
    acc = widgets.Accordion(children=[view_select_out])
    acc.set_title(0, f" View File: {selected_path or '<none>'}")
    display(acc)

    with view_select_out:
        clear_output()
        if not selected_path:
            print(" No output file selected to download.")
            return
        print('selected_path',selected_path)
        data = t.jobs.getJobOutputDownload(jobUuid=jobUuid, outputPath=selected_path)
        text = _bytes_to_text(data, selected_path)
        print(f" Viewing: {selected_path}")

        if text is None:
            print(" (binary file; not displayed here)")
            return

        # Apply line numbers if requested
        display_text = _add_line_numbers(text) if showLineNumbers else text

        nbytes = len(data) if isinstance(data, (bytes, bytearray)) else len(text.encode("utf-8", "ignore"))
        default_view = "pre" if _should_use_pre(display_text, nbytes) else "ta"

        # prepare both widgets once
        html_w = widgets.HTML(
            value=(
                '<pre style="margin:0;white-space:pre;overflow:auto;max-height:500px;'
                'font-family:monospace;">'
                f'{escape(display_text)}'
                '</pre>'
            )
        )
        ta_w = widgets.Textarea(
            value=display_text,
            layout=widgets.Layout(width="100%", height="500px"),
            disabled=False
        )

        # tiny toggle to let the user switch
        toggle = widgets.ToggleButtons(
            options=[("HTML <pre>", "pre"), ("Textarea", "ta")],
            value=default_view, description="Viewer:"
        )
        holder = widgets.Output()
        display(toggle, holder)

        def _render(kind):
            holder.clear_output()
            with holder:
                display(html_w if kind == "pre" else ta_w)

        _render(default_view)
        toggle.observe(lambda ch: (ch["name"] == "value") and _render(ch["new"]), names="value")
