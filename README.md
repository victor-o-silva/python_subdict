# [python] subdict_by_dotted_keys

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
