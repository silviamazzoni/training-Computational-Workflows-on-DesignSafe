def empty_folder(folder_path, delete_folder=False, confirm=True):
    """
    Removes all contents of the specified folder. Optionally deletes the folder itself.

    Parameters
    ----------
    folder_path : str or Path
        Path to the folder to clear.

    delete_folder : bool, optional
        If True, deletes the folder itself after clearing contents.

    confirm : bool, optional
        If True, prompts for confirmation before deleting contents.

    Returns
    -------
    str
        'deleted' if the folder itself was deleted,
        'emptied' if contents were cleared,
        or a string message indicating no action.

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

    from pathlib import Path
    import shutil
    folder = Path(folder_path)

    if not folder.exists():
        print(f"** ERROR ** Folder '{folder}' does not exist.")
        return "folder not found"

    if confirm:
        choice = input(
            f"\nDo you want to clear the contents of\n   \"{folder}\"?"
            f"{' (and delete the folder itself)' if delete_folder else ''} (yes/no/stop): "
        ).strip().lower()
        if choice != 'yes':
            print("Cancelled by user.")
            return "cancelled"

    try:
        if delete_folder:
            shutil.rmtree(folder)
            print(f"Deleted folder '{folder}'.")
            return "deleted"
        else:
            # remove contents but keep the folder
            for item in folder.iterdir():
                if item.is_file() or item.is_symlink():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            print(f"Emptied contents of '{folder}'.")
            return "emptied"
    except Exception as e:
        print(f"** ERROR ** while deleting: {e}")
        return "error"
