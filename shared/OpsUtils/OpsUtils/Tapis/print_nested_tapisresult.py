def print_nested_tapisresult(obj, key0: str = "obj.", indent: int = 0):
    """
    YOU SHOULD USE: display_tapis_results()
    Pretty-print a nested TapisResult/dict/list in a JSON-like, readable form.
    Keys are grouped: scalars → lists → nested dicts. TapisResult objects are
    unwrapped via their internal ``__dict__`` so you can explore schemas/results.

    Behavior
    --------
    - Accepts TapisResult, dict, list, or scalars.
    - Orders keys within dicts as: scalars, then lists, then nested dicts.
    - Lists print inline if simple, or expanded if they contain objects/dicts.
    - Strings are quoted to make the structure clearer.

    Parameters
    ----------
    obj : tapipy.tapis.TapisResult | dict | list | Any
        Object to render. TapisResult values are unwrapped to dictionaries.
    key0 : str, default "obj."
        A prefix for printed keys (useful when showing a named root).
    indent : int, default 0
        Left indentation level (number of two-space blocks).

    Returns
    -------
    None
        Prints to stdout; does not return a value.

    Example
    -------
    # Assuming `schema = t.apps.getAppLatestVersion(appId="opensees-mp-s3")`
    print_nested_tapisresult(schema, key0="schema.")

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
    try:
        from tapipy.tapis import TapisResult
    except Exception:
        class TapisResult:  # sentinel to avoid ImportError during isinstance checks
            pass

    sp = "  " * indent  # current indentation string

    # unwrap TapisResult at the current node
    if isinstance(obj, TapisResult):
        obj = obj.__dict__

    # ---- dict ----
    if isinstance(obj, dict):
        dict_keys, list_keys, scalar_keys = [], [], []
        for k, v in obj.items():
            v_un = v.__dict__ if isinstance(v, TapisResult) else v
            if isinstance(v_un, dict):
                dict_keys.append(k)
            elif isinstance(v_un, list):
                list_keys.append(k)
            else:
                scalar_keys.append(k)

        # print in the order: scalars -> lists -> dicts
        ordered = [*scalar_keys, *list_keys, *dict_keys]
        for idx, k in enumerate(ordered):
            v = obj[k]
            v_un = v.__dict__ if isinstance(v, TapisResult) else v

            # nested dict
            if isinstance(v_un, dict):
                if key0:
                    print(f"{sp}{key0}{k}: " + "{")
                else:
                    print(f"{sp}{k}: " + "{")
                # for nested objects, start with empty prefix so keys don’t double-prefix
                print_nested_tapisresult(v_un, "", indent + 1)
                print(f"{sp}" + "}")

            # list
            elif isinstance(v_un, list):
                label = f"{sp}{key0}{k}: " if key0 else f"{sp}{k}: "
                if not v_un:
                    print(label + "[]")
                else:
                    contains_objects = any(isinstance(it, (dict, TapisResult)) for it in v_un)
                    if contains_objects:
                        print(label + "[")
                        for j, it in enumerate(v_un):
                            it_un = it.__dict__ if isinstance(it, TapisResult) else it
                            if isinstance(it_un, dict):
                                print("  " * (indent + 1) + "{")
                                print_nested_tapisresult(it_un, "", indent + 2)
                                print("  " * (indent + 1) + "}")
                            else:
                                val = f'"{it_un}"' if isinstance(it_un, str) else it_un
                                print("  " * (indent + 1) + f"{val}")
                        print(sp + "]")
                    else:
                        # simple list → inline
                        vals = [f'"{x}"' if isinstance(x, str) else x for x in v_un]
                        print(label + f"[{', '.join(map(str, vals))}]")

            # scalar
            else:
                val = f'"{v_un}"' if isinstance(v_un, str) else v_un
                label = f"{sp}{key0}{k}: " if key0 else f"{sp}{k}: "
                print(label + f"{val}")

    # ---- list (rare at root) ----
    elif isinstance(obj, list):
        if not obj:
            print(sp + "[]")
        else:
            contains_objects = any(isinstance(it, (dict, TapisResult)) for it in obj)
            if contains_objects:
                print(sp + "[")
                for it in obj:
                    it_un = it.__dict__ if isinstance(it, TapisResult) else it
                    if isinstance(it_un, dict):
                        print("  " * (indent + 1) + "{")
                        print_nested_tapisresult(it_un, "", indent + 2)
                        print("  " * (indent + 1) + "}")
                    else:
                        val = f'"{it_un}"' if isinstance(it_un, str) else it_un
                        print("  " * (indent + 1) + f"{val}")
                print(sp + "]")
            else:
                vals = [f'"{x}"' if isinstance(x, str) else x for x in obj]
                print(sp + f"[{', '.join(map(str, vals))}]")

    # ---- scalar ----
    else:
        if isinstance(obj, str):
            print(f"{sp}{key0}{obj}")
        else:
            print(f"{sp}{key0}{obj}")
