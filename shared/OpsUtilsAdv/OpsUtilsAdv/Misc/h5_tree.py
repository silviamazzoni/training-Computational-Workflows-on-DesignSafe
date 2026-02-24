import h5py
def h5_tree(h5: h5py.File, max_items: int = 500, max_depth: int = 6):
    """Print a compact tree of groups/datasets up to max_depth."""
    count = 0

    def _walk(g: h5py.Group, prefix: str, depth: int):
        nonlocal count
        if depth > max_depth:
            return
        for name in g.keys():
            if count >= max_items:
                print("... (stopped: max_items reached)")
                return
            obj = g[name]
            if isinstance(obj, h5py.Group):
                print(f"{prefix}/{name}  [Group]")
                count += 1
                _walk(obj, f"{prefix}/{name}", depth + 1)
            else:
                shape = obj.shape
                dtype = obj.dtype
                print(f"{prefix}/{name}  [Dataset] shape={shape} dtype={dtype}")
                count += 1

    print(f"Tree (max_items={max_items}, max_depth={max_depth}):")
    _walk(h5, "", 0)