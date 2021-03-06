========================
python_subdict
========================

.. image:: https://travis-ci.org/victor-o-silva/python_subdict.svg?branch=master
   :target: https://travis-ci.org/victor-o-silva/python_subdict
   :alt: Build Status

.. image:: https://landscape.io/github/victor-o-silva/python_subdict/master/landscape.svg?style=flat
   :target: https://landscape.io/github/victor-o-silva/python_subdict/master
   :alt: Code Health

.. image:: https://coveralls.io/repos/victor-o-silva/python_subdict/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/victor-o-silva/python_subdict?branch=master
   :alt: Coverage Status

.. image:: https://badge.fury.io/py/subdict.svg
   :target: https://badge.fury.io/py/subdict

The intent of this library is to make it easy to extract subdicts from
python dicts by just specifying which keys are needed, in a
dotted-syntax.

Example
-------------

    >>> from subdict import extract_subdict
    >>> d = {'a': 1, 'b': 0, 'c': {'ca': '3', 'cb': {'cba': 0, 'cbb': False}}}
    >>> extract_subdict(d, ['a', 'c.cb.cbb'])
    {'a': 1, 'c': {'cb': {'cbb': False}}}

Documentation Links
-----------------------

`IPython-Notebook version <https://github.com/victor-o-silva/python_subdict/blob/master/DOCS.ipynb>`_

`Markdown version <https://github.com/victor-o-silva/python_subdict/blob/master/DOCS.md>`_
