import unittest

import responses

from evclient import EVClient


class TestEVClient(unittest.TestCase):
    """
    This class only contains simple init tests for EVClient.
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
            'Authorization': f'Key {self.api_key}',
            'Accept': 'application/json'
        })

    @responses.activate
    def test_api_paths(self) -> None:
        client: EVClient = EVClient(
            domain=self.domain,
            api_key=self.api_key
        )

        with self.subTest('Check that request url contains csv_import api path'):
            responses.add(
                responses.GET,
                url=f'{client._url}/{client._csv_import_api_path}',
                json={'integrations': []},
                status=200
            )
            client.get_csv_imports()
            self.assertEqual(
                responses.calls[len(responses.calls) - 1].request.url,
                f'{client._url}/{client._csv_import_api_path}'
            )

        with self.subTest('Check that request url contains dataset api path'):
            responses.add(
                responses.GET,
                url=f'{client._url}/{client._dataset_api_path}',
                json=[],
                status=200
            )
            client.get_datasets()
            self.assertEqual(
                responses.calls[len(responses.calls) - 1].request.url,
                f'{client._url}/{client._dataset_api_path}'
            )

        with self.subTest('Check that request url contains node api path'):
            responses.add(
                responses.GET,
                url=f'{client._url}/{client._node_api_path}',
                json={'nodes': []},
                status=200
            )
            client.get_nodes()
            self.assertEqual(
                responses.calls[len(responses.calls) - 1].request.url,
                f'{client._url}/{client._node_api_path}'
            )

        with self.subTest('Check that request url contains settings api path'):
            responses.add(
                responses.GET,
                url=f'{client._url}/{client._settings_api_path}/test/1?extract=0',
                json={},
                status=200
            )
            client.get_settings(settings_type='test', settings_id=1)
            self.assertEqual(
                responses.calls[len(responses.calls) - 1].request.url,
                f'{client._url}/{client._settings_api_path}/test/1?extract=0'
            )

        with self.subTest('Check that request url contains tag api path'):
            responses.add(
                responses.GET,
                url=f'{client._url}/{client._tag_api_path}',
                json={'sensors': []},
                status=200
            )
            client.get_tags()
            self.assertEqual(
                responses.calls[len(responses.calls) - 1].request.url,
                f'{client._url}/{client._tag_api_path}'
            )

        with self.subTest('Check that request url contains timeseries api path'):
            responses.add(
                responses.GET,
                url=f'{client._url}/{client._timeseries_api_path}',
                json={'timeseries': []},
                status=200
            )
            client.get_timeseries_data()
            self.assertEqual(
                responses.calls[len(responses.calls) - 1].request.url,
                f'{client._url}/{client._timeseries_api_path}'
            )
