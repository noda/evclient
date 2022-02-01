import unittest
from typing import Union, Dict

from evclient.utils import filter_none_values_from_dict


class TestClientUtils(unittest.TestCase):
    def test_filter_none_values_from_dict(self) -> None:
        with self.subTest('Should only remove key2 because it is None'):
            test_dict: Dict[str, Union[str, bool, int]] = {
                'key1': 'value1',
                'key2': None,
                'key3': '',
                'key4': False,
                'key5': 0
            }
            result: Dict = filter_none_values_from_dict(test_dict)
            self.assertEqual(result, {
                'key1': 'value1',
                'key3': '',
                'key4': False,
                'key5': 0
            })
