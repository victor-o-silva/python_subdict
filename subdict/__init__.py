import sys
PYTHON3 = sys.version_info.major > 2


def get_dotted_keys(_dict, prefix=None):
    """Return all valid dotted-syntax keys of a dict.

    Parameters
    ----------
    _dict : dict
        The checked dict.
    prefix : str, optional
        If passed, all keys will have `prefix` + "." (a dot) as a prefix.

    Examples
    ----------
    >>> d = {'a': 1, 'b': 0, 'c': {'ca': '3', 'cb': {'cba': 0, 'cbb': False}}}
    >>> sorted(get_dotted_keys(d))
    ['a', 'b', 'c', 'c.ca', 'c.cb', 'c.cb.cba', 'c.cb.cbb']
    """
    keys = []
    for key, value in (_dict.items() if PYTHON3 else _dict.iteritems()):
        if isinstance(value, dict):
            if prefix is None:
                _prefix = key
            else:
                _prefix = '%s.%s' % (prefix, key)
            keys.append(_prefix)
            keys.extend(get_dotted_keys(value, prefix=_prefix))
        else:
            if prefix is not None:
                keys.append('%s.%s' % (prefix, key))
            else:
                keys.append(key)
    return keys


def get_item(_dict, dotted_key):
    """Return an item from a dict by a dotted-syntax-key.

    Parameters
    ----------
    _dict : dict
        The checked dict.
    dotted_key : str
        The looked-up key, in dotted-syntax (e.g: 'company.address.city')

    Raises
    ------
    KeyError
        If the key is invalid.

    Examples
    ----------
    >>> d = {'employee': {'name': 'Alex', 'company': {'name': 'XPTO'}}}
    >>> get_item(d, 'employee.name')
    'Alex'
    >>> get_item(d, 'employee.company')
    {'name': 'XPTO'}

    """
    value = _dict.copy()
    for subkey in dotted_key.split('.'):
        value = value[subkey]
    return value


def set_item(_dict, dotted_key, value):
    """Set a value to the proper dotted-syntax-key in a dict (in-place).

    Creates intermediate dicts as needed.

    Parameters
    ----------
    _dict : dict
        The changed dict.
    dotted_key : str
        The key, in dotted-syntax.
    value
        The value to be set.

    Examples
    ----------
    >>> d = {}
    >>> set_item(d, 'b.a', True)
    >>> d
    {'b': {'a': True}}

    """
    key_parts = dotted_key.split('.')
    last_part_index = len(key_parts) - 1
    aux_dict = _dict
    for index, key_part in enumerate(key_parts):
        if index < last_part_index:
            if key_part not in aux_dict:
                aux_dict[key_part] = {}
            aux_dict = aux_dict[key_part]
            assert isinstance(aux_dict, dict)
        else:
            aux_dict[key_part] = value


def extract_subdict(dictionary, keys=None, strict=False):
    """Return a subdict of a dict, only with the specified dotted-syntax keys.

    Parameters
    ----------
    dictionary : dict
        The original dict, from which the subdict will be extracted.
    keys : list of strings, optional
        Keys, in dotted-syntax (e.g: 'person.name', 'company.address.city'),
        from the original dict that must be in the subdict.
    strict : bool, optional
        If True, raises a KeyError if any of the `keys` is invalid.
        If False (the default value), invalid keys are ignored.

    Raises
    ------
    KeyError
        If at least one key is invalid AND `strict` is True.

    Examples
    ----------
    >>> from pprint import pprint
    >>> d = {'a': 1, 'b': 0, 'c': {'ca': '3', 'cb': {'cba': 0, 'cbb': False}}}
    >>> pprint(extract_subdict(d, ['a', 'c.cb.cbb']))
    {'a': 1, 'c': {'cb': {'cbb': False}}}
    """
    if keys is None:
        return dictionary.copy()

    _dict = {}

    available_keys = get_dotted_keys(dictionary)
    for dotted_key in keys:
        if dotted_key in available_keys:
            value = get_item(dictionary, dotted_key)
            set_item(_dict, dotted_key, value)
        else:
            if strict:
                raise KeyError(dotted_key)

    return _dict
