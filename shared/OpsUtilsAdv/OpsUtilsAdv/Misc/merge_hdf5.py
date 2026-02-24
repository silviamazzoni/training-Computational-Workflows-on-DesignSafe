#!/usr/bin/env python3
"""
Merge multiple HDF5 files into one output HDF5.

- Copies full HDF5 tree (groups, datasets, attributes)
- Preserves dataset layout (compression/chunks) via HDF5 copy
- Conflict policies: skip | overwrite | error
- Optional prefixing: put each input under /<prefixN>/... to avoid collisions

Author: Silvia Mazzoni (silviamazzoni@yahoo.com)
"""

from __future__ import annotations

import os
from typing import Iterable, Optional

import h5py
import csv

def merge_hdf5_files(
    inputs: list[str],
    output: str,
    conflict: str = "skip",                 # "error"|"skip"|"overwrite"
    collisions_csv="", # new
    prefix_mode: str = "none",               # "none"|"filename"|"index"
    include_paths: Optional[list[str]] = None,  # e.g. ["/RSN"]
    exclude_prefixes: Optional[list[str]] = None,
    copy_root_attrs: bool = False,
    verbose: bool = False,
) -> None:
    """
    Merge multiple HDF5 files into a single output.

    - Preserves dataset layout (chunks/compression/filters) via HDF5 copy.
    - Optionally merges only selected subtrees (include_paths).
    - Optional prefixing avoids collisions by placing each input under a group.

    Author: Silvia Mazzoni (silviamazzoni@yahoo.com)
    """
    collisions = []  # list of dicts
    if conflict not in {"skip", "overwrite", "error"}:
        raise ValueError("conflict must be one of: skip, overwrite, error")
    if prefix_mode not in {"none", "filename", "index"}:
        raise ValueError("prefix_mode must be one of: none, filename, index")

    out_abs = os.path.abspath(output)
    in_abs = [os.path.abspath(p) for p in inputs]
    if out_abs in set(in_abs):
        raise RuntimeError("Output file is also listed as an input.")

    for p in inputs:
        if not os.path.exists(p):
            raise FileNotFoundError(p)

    os.makedirs(os.path.dirname(out_abs) or ".", exist_ok=True)

    include_paths = include_paths or ["/"]  # default: whole file
    exclude_prefixes = exclude_prefixes or []

    def _safe_group_name(s: str) -> str:
        base = os.path.basename(s)
        stem = os.path.splitext(base)[0]
        return "".join(ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in stem)

    def _should_exclude(path: str) -> bool:
        return any(path.startswith(x.rstrip("/") + "/") or path == x.rstrip("/") for x in exclude_prefixes)

    def _iter_paths_under(src: h5py.File, root: str) -> list[str]:
        """Return all group/dataset paths under root (excluding root itself)."""
        out: list[str] = []
        root = root.rstrip("/")
        if root == "":
            root = "/"
        if root != "/" and root not in src:
            return out

        def visitor(name: str, obj):
            p = "/" + name
            if root == "/":
                out.append(p)
            else:
                if p.startswith(root + "/") and p != root:
                    out.append(p)

        src.visititems(visitor)
        # parents first
        out.sort(key=lambda p: (p.count("/"), p))
        # exclude the include root if it shows up (it can)
        out = [p for p in out if p != root]
        return out

    with h5py.File(out_abs, "w") as dst:
        for idx, in_path in enumerate(inputs):
            if prefix_mode == "none":
                prefix = ""
            elif prefix_mode == "index":
                prefix = f"/file_{idx+1}"
                dst.require_group(prefix)
            else:  # filename
                prefix = "/" + _safe_group_name(in_path)
                dst.require_group(prefix)

            with h5py.File(in_path, "r") as src:
                # Optionally copy root attrs into the destination root (or prefix group)
                if copy_root_attrs:
                    target = dst[prefix] if prefix else dst["/"]
                    for k in src["/"].attrs.keys():
                        if conflict == "error" and k in target.attrs:
                            raise RuntimeError(f"Root attribute conflict: {k}")
                        if conflict == "skip" and k in target.attrs:
                            continue
                        try:
                            target.attrs[k] = src["/"].attrs[k]
                        except Exception:
                            pass

                for inc in include_paths:
                    inc = inc.rstrip("/") or "/"
                    paths = _iter_paths_under(src, inc)

                    # If include root itself is a dataset/group and you want it copied too:
                    if inc != "/" and inc in src and not _should_exclude(inc):
                        paths = [inc] + paths

                    for sp in paths:
                        if _should_exclude(sp):
                            continue
                        # destination path mirrors source path, with optional prefix
                        dp = prefix + sp

                        if dp in dst:
                            collisions.append({"path": dp, "source_file": in_path, "action": conflict})
                            if conflict == "skip":
                                if verbose: print(f"[skip] {dp} from {in_path}")
                                continue
                            if conflict == "overwrite":
                                if verbose: print(f"[overwrite] {dp} from {in_path}")
                                del dst[dp]
                            if conflict == "error":
                                raise RuntimeError(f"Conflict at destination path: {dp}")

                        # Copy into parent group
                        parent = os.path.dirname(dp.rstrip("/")) or "/"
                        name = os.path.basename(dp.rstrip("/"))
                        dst.require_group(parent)
                        dst[parent].copy(src[sp], name)

                        if verbose:
                            print(f"[copy] {sp} -> {dp}")
    # after merge finishes:
    if collisions:
        if len(collisions_csv)==0:
            
            collisions_csv = f'{output}_collisions.csv'
        with open(collisions_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["path", "source_file", "action"])
            w.writeheader()
            w.writerows(collisions)
        if verbose:
            print(f"Wrote collisions log: {collisions_csv} (n={len(collisions)})")



