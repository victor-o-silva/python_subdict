import unittest
from extract_subdict import (extract_subdict, get_dotted_keys,
                             get_item, set_item)


# Auxiliar functions' tests

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dict = {
            'name': 'Sherlock Holmes',
            'address': {
                'street': {'type': 'Street', 'name': 'Baker'},
                'number': '221B', 'city': 'London', 'country': 'England',
            },
            'books': ['A Study in Scarlet', 'The Sign of the Four',
                      'The Adventures of Sherlock Holmes']
        }


class GetDottedKeys(BaseTestCase):
    def test_no_prefix(self):
        sorted_keys = sorted(get_dotted_keys(self.test_dict))
        self.assertEqual(sorted_keys, [
            'address', 'address.city', 'address.country',
            'address.number', 'address.street', 'address.street.name',
            'address.street.type', 'books', 'name',
        ])

    def test_with_prefix(self):
        sorted_keys = sorted(get_dotted_keys(self.test_dict, 'data'))
        self.assertEqual(sorted_keys, [
            'data.address', 'data.address.city', 'data.address.country',
            'data.address.number', 'data.address.street',
            'data.address.street.name', 'data.address.street.type',
            'data.books', 'data.name',
        ])


class GetItem(BaseTestCase):
    def test_get_valid_items(self):
        self.assertEqual(get_item(self.test_dict, 'name'), 'Sherlock Holmes')
        self.assertEqual(get_item(self.test_dict, 'books'), [
            'A Study in Scarlet', 'The Sign of the Four',
            'The Adventures of Sherlock Holmes'
        ])
        self.assertEqual(get_item(self.test_dict, 'address'), {
            'street': {'type': 'Street', 'name': 'Baker'},
            'number': '221B', 'city': 'London', 'country': 'England'
        })
        self.assertEqual(get_item(self.test_dict, 'address.city'), 'London')
        self.assertEqual(
            get_item(self.test_dict, 'address.street.name'),
            'Baker'
        )

    def test_get_invalid_items(self):
        with self.assertRaises(KeyError) as cm:
            get_item(self.test_dict, 'birth_date')
        self.assertEqual(cm.exception.message, 'birth_date')

        with self.assertRaises(KeyError) as cm:
            get_item(self.test_dict, 'address.postal_code')
        self.assertEqual(cm.exception.message, 'postal_code')

        with self.assertRaises(KeyError) as cm:
            get_item(self.test_dict, 'address.street.old_name')
        self.assertEqual(cm.exception.message, 'old_name')


class SetItem(BaseTestCase):
    def test_set_items(self):
        d = {}

        set_item(d, 'a', 1)
        self.assertEqual(d, {'a': 1})

        set_item(d, 'b.a', True)
        self.assertEqual(d, {'a': 1, 'b': {'a': True}})

        set_item(d, 'b.b', {'hey': 'oh', 'lets': 'go'})
        self.assertEqual(d, {
            'a': 1,
            'b': {'a': True, 'b': {'hey': 'oh', 'lets': 'go'}}
        })

        set_item(d, 'c.d.e', 42)
        self.assertEqual(d, {
            'a': 1,
            'b': {'a': True, 'b': {'hey': 'oh', 'lets': 'go'}},
            'c': {'d': {'e': 42}}
        })


# Main function's tests


class ExtractSubdict(BaseTestCase):
    def test_extract_valid_keys(self):
        self.assertEqual(extract_subdict(self.test_dict), self.test_dict)

        self.assertEqual(
            extract_subdict(self.test_dict, ['name', 'books']),
            {
                'name': 'Sherlock Holmes',
                'books': [
                    'A Study in Scarlet', 'The Sign of the Four',
                    'The Adventures of Sherlock Holmes'
                ]
            }
        )

        self.assertEqual(
            extract_subdict(self.test_dict, ['name', 'address']),
            {
                'name': 'Sherlock Holmes',
                'address': {
                    'street': {'type': 'Street', 'name': 'Baker'},
                    'number': '221B', 'city': 'London', 'country': 'England',
                },
            }
        )

        self.assertEqual(
            extract_subdict(self.test_dict, ['name', 'address.street',
                                             'address.country']),
            {
                'name': 'Sherlock Holmes',
                'address': {
                    'street': {'type': 'Street', 'name': 'Baker'},
                    'country': 'England',
                },
            }
        )

        self.assertEqual(
            extract_subdict(self.test_dict, ['name', 'address.street.type',
                                             'address.city']),
            {
                'name': 'Sherlock Holmes',
                'address': {'street': {'type': 'Street'}, 'city': 'London'},
            }
        )

    def test_extract_invalid_keys(self):
        self.assertEqual(
            extract_subdict(self.test_dict, ['name', 'invalid']),
            {'name': 'Sherlock Holmes'}
        )

        with self.assertRaises(KeyError) as cm:
            extract_subdict(self.test_dict, ['name', 'invalid'], strict=True)
        self.assertEqual(cm.exception.message, 'invalid')


if __name__ == '__main__':
    unittest.main()
