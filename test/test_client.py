import unittest

from evclient import EVClient


class TestEVClient(unittest.TestCase):
    """
    This class only contains a simple test for initializing EVClient.
    In-depth testing of the functionality can be found in the test files for
    the client classes that EVClient inherits from.
    """
    def setUp(self) -> None:
        self.domain: str = 'test'
        self.api_key: str = '123456789'

    def test_credentials_from_input_params(self) -> None:
        client: EVClient = EVClient(
            domain=self.domain,
            api_key=self.api_key
        )
        self.assertEqual(client._domain, self.domain)
        self.assertEqual(client._session.headers, {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        })
