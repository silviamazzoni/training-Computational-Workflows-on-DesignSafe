def get_dictlist_keys(dict_list,key_label='key'):
    """
    Return a list of all key_label names from a list of dictionaries.

    Parameters
    ----------
    dict_list : list of dict
        The environment variable objects, each containing a key_label.
    key_label : str
        The name of the key to search for.
            

    Returns
    -------
    list of str
        All key names found in the list.
    """
    return [item.get(key_label) for item in dict_list]
