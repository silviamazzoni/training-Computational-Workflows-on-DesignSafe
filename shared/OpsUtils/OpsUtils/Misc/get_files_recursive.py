def get_files_recursive(path: str = "", displayIt=10, returnItems: bool = False, displayLevel: int = 0):
    """
    Recursively list files under a directory with optional on-screen display and
    a structured return payload.

    Features
    --------
    - Recursively walks `path`, listing files before directories at each level.
    - Optional display of file paths with a limit per directory level.
      * If `displayIt` is `True`, displays all files.
      * If `displayIt` is `False`, displays nothing.
      * If `displayIt` is an `int >= 2`, displays up to that many files per directory; prints a suppression note afterward.
    - Returns counts and paths when `returnItems=True`.

    Parameters
    ----------
    path : str, default=""
        Directory to traverse. Empty string means current working directory (`"."`).
    displayIt : bool | int, default=10
        Controls on-screen printing:
        * `True`  -> print everything
        * `False` -> print nothing
        * `int` (>=2) -> print up to that many files per directory level
        * `int` (0 or 1) -> treated as no limit (prints everything at that level)
    returnItems : bool, default=False
        If `True`, return a dict with counts and path lists (see Returns).
    displayLevel : int, default=0
        Internal recursion depth; callers generally leave this at default.

    Returns
    -------
    dict | None
        If `returnItems=True`, returns:
            {
                'Nfiles': <int>,                 # total number of files found
                'LocalPath': <list[str]>,        # relative paths from `path`
                'FullPath': <list[str]>,         # absolute file paths
                'Items': <list[str]>             # basenames of files
            }
        Otherwise returns `None`.

    Notes
    -----
    - Skips directories named `.ipynb_checkpoints`.
    - Files are displayed before directories at each level for readability.
    - Paths in `LocalPath` are relative to the input `path` (or "." if empty).

    Example
    -------
    # Print up to 10 files per directory and also capture the results:
    results = get_files_recursive("data", displayIt=10, returnItems=True)
    print("Total files:", results['Nfiles'])

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

    import os

    # Interpret displayIt
    if isinstance(displayIt, bool):
        if displayLevel == 0:
            displayLevel = 1 if displayIt else 0
        displayLimit = None  # no per-dir limit; print all/none based on displayLevel
    elif isinstance(displayIt, int):
        if displayLevel == 0:
            displayLevel = 1  # enable display at top if an int was provided
        displayLimit = displayIt if displayIt >= 2 else None
    else:
        displayLimit = None

    # Print directory header at this level if enabled
    if displayLevel == 1:
        print('----------------------------')
        print(f'\nDIRECTORY: {path if path else "."}')

    # Prepare accumulators (use distinct names; do not overwrite the flag)
    Nfiles = 0
    local_paths = []
    full_paths = []
    item_names = []

    # Resolve the output path
    root = path if path else "."
    try:
        entries = os.listdir(root)
    except FileNotFoundError:
        if displayLevel == 1:
            print(f'  [Error] Directory not found: {root}')
        return {'Nfiles': 0, 'LocalPath': [], 'FullPath': [], 'Items': []} if returnItems else None
    except PermissionError:
        if displayLevel == 1:
            print(f'  [Error] Permission denied: {root}')
        return {'Nfiles': 0, 'LocalPath': [], 'FullPath': [], 'Items': []} if returnItems else None

    # Split into files vs directories (files first in display)
    dirs = [e for e in entries if os.path.isdir(os.path.join(root, e))]
    files = [e for e in entries if not os.path.isdir(os.path.join(root, e))]
    ordered = files + dirs

    if displayLevel == 1:
        print(f'  {len(files)} files & {len(dirs)} directories:')

    printed_count = 0
    suppressed_note_shown = False

    for name in ordered:
        if name == '.ipynb_checkpoints':
            continue

        local = name if not path else os.path.join(path, name)
        full = os.path.abspath(os.path.join(root, name))

        if os.path.isdir(full):
            # Print directory header for subdir when displaying
            if displayLevel == 1:
                print('----------------------------')
                print(f'\nDIRECTORY: {local}')

            # Recurse
            ret = get_files_recursive(local, displayIt=displayIt, returnItems=True, displayLevel=displayLevel + 1)
            Nfiles += ret['Nfiles']
            local_paths.extend(ret['LocalPath'])
            full_paths.extend(ret['FullPath'])
            item_names.extend(ret['Items'])
        else:
            # Record file
            Nfiles += 1
            local_paths.append(local)
            full_paths.append(full)
            item_names.append(name)

            # Conditional display
            if displayLevel == 1:
                if displayLimit is None or printed_count < displayLimit:
                    print(f'    FILE: {local}')
                    printed_count += 1
                    if displayLimit is not None and printed_count == displayLimit:
                        # next files will be suppressed
                        pass
                elif not suppressed_note_shown:
                    print(f'\n          ........(suppressing additional-file display beyond {displayLimit})')
                    suppressed_note_shown = True

    if returnItems:
        return {
            'Nfiles': Nfiles,
            'LocalPath': local_paths,
            'FullPath': full_paths,
            'Items': item_names
        }
