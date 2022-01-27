import responses
import unittest
import urllib
from typing import Dict

from evclient import SettingsClient


class TestSettingsClient(unittest.TestCase):
    def setUp(self) -> None:
        self.domain: str = 'test'
        self.api_key: str = '123456789'
        self.client: SettingsClient = SettingsClient(
            domain=self.domain,
            api_key=self.api_key
        )
        self.settings_type = 'node'
        self.settings_id = 1

    @responses.activate
    def test_get_settings(self) -> None:
        mock_response: Dict = {
            'coco': {
                'default': {
                    'control': {
                        'balance_temperature': 17,
                        'bias_hour_cap_charge': -30,
                        'bias_hour_cap_discharge': 32,
                        'bias_hour_recovery_time': 24
                    }
                }
            }
        }

        responses.add(
            responses.GET,
            url=f'{self.client._url}/{self.client._api_path}/{self.settings_type}/{self.settings_id}',
            json=mock_response,
            status=200
        )

        with self.subTest('call successful with complete parameter list and extract param is True'):
            params: Dict[str, str] = {
                'path': 'coco',
                'extract': True
            }

            res: Dict = self.client.get_settings(self.settings_type, self.settings_id, **params)

            self.assertEqual(res, mock_response)
            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._api_path}/{self.settings_type}/{self.settings_id}'
                f'?{urllib.parse.urlencode({"path": params["path"], "extract": 1})}'
            )
            self.assertEqual(responses.calls[0].request.params.get('path'), str(params['path']))
            self.assertEqual(responses.calls[0].request.params.get('extract'), str(1))

        with self.subTest('call successful with complete parameter list and extract param is omitted'):
            params: Dict[str, str] = {
                'path': 'coco',
            }

            res: Dict = self.client.get_settings(self.settings_type, self.settings_id, **params)

            self.assertEqual(res, mock_response)
            self.assertEqual(len(responses.calls), 2)

            self.assertEqual(
                responses.calls[1].request.url,
                f'{self.client._url}/{self.client._api_path}/{self.settings_type}/{self.settings_id}'
                f'?{urllib.parse.urlencode({"path": params["path"], "extract": 0})}'
            )
            self.assertEqual(responses.calls[1].request.params.get('path'), str(params['path']))
            self.assertEqual(responses.calls[1].request.params.get('extract'), str(0))

    @responses.activate
    def test_store_settings(self) -> None:
        mock_response: Dict = {
            'value': '1'
        }

        responses.add(
            responses.PUT,
            url=f'{self.client._url}/{self.client._api_path}/{self.settings_type}/{self.settings_id}',
            json=mock_response,
            status=200
        )

        with self.subTest('call successful with complete parameter list and force param is True'):
            params: Dict[str, str] = {
                'path': 'coco',
                'value': '1',
                'force': True
            }

            res: Dict = self.client.store_settings(self.settings_type, self.settings_id, **params)

            self.assertEqual(res, mock_response)
            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._api_path}/{self.settings_type}/{self.settings_id}'
            )
            body_params: Dict[str, str] = urllib.parse.parse_qs(responses.calls[0].request.body)
            self.assertEqual(body_params['path'][0], params['path'])
            self.assertEqual(body_params['value'][0], params['value'])
            self.assertEqual(body_params['force'][0], '1')

        with self.subTest('call successful with complete parameter list and force param is omitted'):
            params: Dict[str, str] = {
                'path': 'coco',
                'value': '1',
            }

            res: Dict = self.client.store_settings(self.settings_type, self.settings_id, **params)

            self.assertEqual(res, mock_response)
            self.assertEqual(len(responses.calls), 2)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._api_path}/{self.settings_type}/{self.settings_id}'
            )
            body_params: Dict[str, str] = urllib.parse.parse_qs(responses.calls[1].request.body)
            self.assertEqual(body_params['path'][0], params['path'])
            self.assertEqual(body_params['value'][0], params['value'])
            self.assertFalse('force' in body_params)
