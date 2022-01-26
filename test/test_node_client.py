import responses
import unittest

from evclient import NodeClient, NodeResponse


class TestNodeClient(unittest.TestCase):
    def setUp(self) -> None:
        self.domain: str = 'test'
        self.api_key: str = '123456789'
        self.client: NodeClient = NodeClient(
            domain=self.domain,
            api_key=self.api_key
        )

    @responses.activate
    def test_get_csv_imports(self) -> None:
        mock_response: NodeResponse = {
            'nodes': [
                {
                    'id': 60,
                    'uuid': 'ccb286c5-d13f-4083-9e02-db2d5bafe27b',
                    'name': 'Exempel heatingsystem',
                    'description': '',
                    'public': True,
                    'owner': False,
                    'enabled': True,
                    'archived': False,
                    'representation': 'circuit/heat',
                    'device': {
                        'id': 1,
                        'name': 'Kelp-Basic',
                        'protocol_id': 1
                    },
                    'sensor_ids': [
                        398,
                        1,
                        42,
                        9,
                        3,
                        121
                    ],
                    'interval': 600
                }
            ]
        }
        with self.subTest('call successful with complete parameter list'):
            responses.add(
                responses.GET,
                url=f'{self.client._url}/{self.client._api_path}',
                json=mock_response,
                status=200
            )

            res: NodeResponse = self.client.get_nodes()

            self.assertEqual(res, mock_response)
            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._api_path}'
            )
