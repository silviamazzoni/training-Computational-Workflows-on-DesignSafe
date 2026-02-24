def get_dictlist_value(dict_list, key_name, key_label='key',value_label='value',default=None):
    """
    Return the 'value' associated with a given 'key' in a list of
    Tapis-style environment variable dictionaries.

    Parameters
    ----------
    dict_list : list of dict
        The environment variable objects, each containing key_label and value_label.
    key_name : str
        The key to search for.
    key_label : str
        The name of the key to search for.
    value_label : str
        The name of the value to search for.
    default : any, optional
        Value to return if key is not found. Default is None.

    Returns
    -------
    any
        The corresponding 'value' if found, otherwise `default`.
    """
    return next(
        (item.get(value_label) for item in dict_list if item.get(key_label) == key_name),
        default
    )
