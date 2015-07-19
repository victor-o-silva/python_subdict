
# python_subdict

The intent of this library is to make it easy to extract subdicts from python dicts by just specifying which keys are needed, in a dotted-syntax.

As an example, let's say that we have the following dict:


    d = {
        'a': 'A',
        'b': 'B',
        'c': 'C',
        'd': {
            'x': 'D_X',
            'y': 'D_Y',
            'z': {
                'I': 'D_Z_I',
                'II': {
                    '1': 'D_Z_II_1',
                    '2': 'D_Z_II_2'
                },
                'III': 'D_Z_III'
            }
        }
    }

If we need only the keys `'a'` and `'d'`, we can do this:


    from extract_subdict import extract_subdict  # The main function of the library


    from pprint import pprint  # Just for a nice presentation here


    pprint( extract_subdict(d, ['a', 'd']) )

    {'a': 'A',
     'd': {'x': 'D_X',
           'y': 'D_Y',
           'z': {'I': 'D_Z_I',
                 'II': {'1': 'D_Z_II_1', '2': 'D_Z_II_2'},
                 'III': 'D_Z_III'}}}


We can also specify 'subkeys' by using a dotted-syntax:


    pprint( extract_subdict(d, ['a', 'd.x', 'd.z']) )

    {'a': 'A',
     'd': {'x': 'D_X',
           'z': {'I': 'D_Z_I',
                 'II': {'1': 'D_Z_II_1', '2': 'D_Z_II_2'},
                 'III': 'D_Z_III'}}}


The dotted-syntax can have any needed level of depth:


    pprint( extract_subdict(d, ['a', 'd.z.II.1']) )

    {'a': 'A', 'd': {'z': {'II': {'1': 'D_Z_II_1'}}}}


# Specifying invalid keys behavior

Let's consider the following dict from now:


    person = {
        'name': 'John Frusciante',
        'birth': '1970-03-05',
        'city': {
            'name': 'New York City',
            'state': {'name': 'New York', 'country': 'USA'}
        },
        'albums': [
            {
                'year': 2001,
                'name': 'To Record Only Water For Ten Days',
                'label': {
                    'name': 'Warner Bros Records',
                    'link': 'https://en.wikipedia.org/wiki/Warner_Bros._Records'
                }
            },
            {
                'year': 2004,
                'name': 'Shadows Collide With People',
                'label': {
                    'name': 'Warner Bros Records',
                    'link': 'https://en.wikipedia.org/wiki/Warner_Bros._Records'
                }
            },
            {
                'year': 2009,
                'name': 'The Empyrean',
                'label': {
                    'name': 'Record Collection',
                    'link': 'https://en.wikipedia.org/wiki/Record_Collection'
                }
            }
        ]
    }

By default, invalid keys passed to the `extract_subdict` function are ignored:


    extract_subdict(person, ['name', 'birth', 'hair_color'])  # 'hair_color' is not present in the `person` dict




    {'birth': '1970-03-05', 'name': 'John Frusciante'}



However, by passing `True` to the `strict` parameter of the function, invalid keys will raise a `KeyError` exception:


    extract_subdict(person, ['name', 'birth', 'hair_color'], strict=True)


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    <ipython-input-9-d854ccf3d6ff> in <module>()
    ----> 1 extract_subdict(person, ['name', 'birth', 'hair_color'], strict=True)
    

    /home/victor/code/python_subdict/extract_subdict.pyc in extract_subdict(dictionary, keys, strict)
        135         else:
        136             if strict:
    --> 137                 raise KeyError(dotted_key)
        138 
        139     return _dict


    KeyError: 'hair_color'


# Successive extractions

Extracting only `'name'` and `'albums'` from the `person` dict:


    subdict = extract_subdict(person, ['name', 'albums'])


    pprint(subdict)

    {'albums': [{'label': {'link': 'https://en.wikipedia.org/wiki/Warner_Bros._Records',
                           'name': 'Warner Bros Records'},
                 'name': 'To Record Only Water For Ten Days',
                 'year': 2001},
                {'label': {'link': 'https://en.wikipedia.org/wiki/Warner_Bros._Records',
                           'name': 'Warner Bros Records'},
                 'name': 'Shadows Collide With People',
                 'year': 2004},
                {'label': {'link': 'https://en.wikipedia.org/wiki/Record_Collection',
                           'name': 'Record Collection'},
                 'name': 'The Empyrean',
                 'year': 2009}],
     'name': 'John Frusciante'}


Extracting only the `'name'` of each album:


    for index in range(len(subdict['albums'])):
        subdict['albums'][index] = extract_subdict(subdict['albums'][index], ['name'])


    pprint(subdict)

    {'albums': [{'name': 'To Record Only Water For Ten Days'},
                {'name': 'Shadows Collide With People'},
                {'name': 'The Empyrean'}],
     'name': 'John Frusciante'}



    
