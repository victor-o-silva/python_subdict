def get_dotted_keys(_dict, prefix=None):
    """Return all valid dotted-notation keys of a dict.

    Parameters
    ----------
    _dict : dict
        The checked dict.
    prefix : str, optional
        If passed, all keys will have `prefix` + "." (a dot) as a prefix.

    >>> d = {'a': 1, 'b': 'test', 'c': None, 'd': {'da': '3', 'db': 1.25, 'dc': {'dca': 0, 'dcb': False}}}

    >>> sorted(get_dotted_keys(d))
    ['a', 'b', 'c', 'd', 'd.da', 'd.db', 'd.dc', 'd.dc.dca', 'd.dc.dcb']

    >>> sorted(get_dotted_keys(d, prefix='test'))
    ['test.a', 'test.b', 'test.c', 'test.d', 'test.d.da', 'test.d.db', 'test.d.dc', 'test.d.dc.dca', 'test.d.dc.dcb']

    >>> get_dotted_keys({})
    []
    """
    keys = []
    for key, value in _dict.iteritems():
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
    """Return an item from a dict by a dotted-notation-key.

    Parameters
    ----------
    _dict : dict
        The checked dict.
    dotted_key : str
        The looked-up key, in dotted-notation (e.g: 'person.name', 'company.address.city')

    Raises
    ------
    KeyError
        If the key is invalid.

    >>> from pprint import pprint
    >>> d = {'a': 1, 'b': 'test', 'c': None, 'd': {'da': '3', 'db': 1.25, 'dc': {'dca': 0, 'dcb': False}}}

    >>> get_item(d, 'a')
    1

    >>> pprint(get_item(d, 'd'), width=120)
    {'da': '3', 'db': 1.25, 'dc': {'dca': 0, 'dcb': False}}

    >>> pprint(get_item(d, 'd.dc'), width=120)
    {'dca': 0, 'dcb': False}

    >>> get_item(d, 'd.dc.dcb')
    False

    >>> pprint(get_item(d, 'error'), width=120)
    Traceback (most recent call last):
        ...
    KeyError: 'error'

    >>> pprint(get_item(d, 'd.dy.dcz'), width=120)
    Traceback (most recent call last):
        ...
    KeyError: 'dy'
    """
    value = _dict.copy()
    for subkey in dotted_key.split('.'):
        value = value[subkey]
    return value


def set_item(_dict, dotted_key, value):
    """Set a value to the proper dotted-notation-key in a dict (in-place).

    Creates intermediate dicts as needed.

    Parameters
    ----------
    _dict : dict
        The changed dict.
    dotted_key : str
        The key, in dotted-notation
    value
        The value to be set.

    >>> from pprint import pprint
    >>> d = {}

    >>> set_item(d, 'a', 1)
    >>> pprint(d, width=120)
    {'a': 1}

    >>> set_item(d, 'b.a', True)
    >>> pprint(d, width=120)
    {'a': 1, 'b': {'a': True}}

    >>> set_item(d, 'b.b', {'hey': 'oh', 'lets': 'go'})
    >>> pprint(d, width=120)
    {'a': 1, 'b': {'a': True, 'b': {'hey': 'oh', 'lets': 'go'}}}

    >>> set_item(d, 'c.d.e', 42)
    >>> pprint(d, width=120)
    {'a': 1, 'b': {'a': True, 'b': {'hey': 'oh', 'lets': 'go'}}, 'c': {'d': {'e': 42}}}
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


def extract_subdict(dictionary, fields=None):
    """Return a subdict of a dict, only with the specified keys.

    Parameters
    ----------
    dictionary : dict
        The original dict, from which the subdict will be extracted.
    fields : list of strings, optional
        Keys, in dotted-notation (e.g: 'person.name', 'company.address.city'),
        from the original dict that must be in the subdict.

    >>> from pprint import pprint
    >>> d = {'a': 1, 'b': 'test', 'c': None, 'd': {'da': '3', 'db': 1.25, 'dc': {'dca': 0, 'dcb': False}}}

    >>> pprint(extract_subdict(d), width=120)
    {'a': 1, 'b': 'test', 'c': None, 'd': {'da': '3', 'db': 1.25, 'dc': {'dca': 0, 'dcb': False}}}

    >>> pprint(extract_subdict(d, ['a', 'b', 'c']), width=120)
    {'a': 1, 'b': 'test', 'c': None}

    >>> pprint(extract_subdict(d, ['c', 'd']), width=120)
    {'c': None, 'd': {'da': '3', 'db': 1.25, 'dc': {'dca': 0, 'dcb': False}}}

    >>> pprint(extract_subdict(d, ['c', 'd.da', 'd.dc']), width=120)
    {'c': None, 'd': {'da': '3', 'dc': {'dca': 0, 'dcb': False}}}

    >>> pprint(extract_subdict(d, ['d.dc.dcb']), width=120)
    {'d': {'dc': {'dcb': False}}}
    """
    if fields is None:
        return dictionary.copy()

    _dict = {}

    available_keys = get_dotted_keys(dictionary)
    for dotted_key in fields:
        assert dotted_key in available_keys, '%r not in %r' % (dotted_key, available_keys)
        value = get_item(dictionary, dotted_key)
        set_item(_dict, dotted_key, value)

    return _dict


if __name__ == "__main__":
    import doctest
    doctest.testmod()
