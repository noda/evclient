import unittest

from evclient.utils import filter_none_values_from_dict


class TestPCTBaseClient(unittest.TestCase):
    def test_filter_none_values_from_dict(self):
        with self.subTest('Should only remove key2 because it is None'):
            test_dict = {
                'key1': 'value1',
                'key2': None,
                'key3': '',
                'key4': False,
                'key5': 0
            }
            result = filter_none_values_from_dict(test_dict)
            self.assertEqual(result, {
                'key1': 'value1',
                'key3': '',
                'key4': False,
                'key5': 0
            })
