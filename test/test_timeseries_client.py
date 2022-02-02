import json

import responses
import unittest
import urllib
from typing import Dict, Any, Optional

from evclient import TimeseriesClient, TimeseriesResponse, TimeseriesDataResponse, TimeseriesType


class TestTimeseriesClient(unittest.TestCase):
    def setUp(self) -> None:
        self.domain: str = 'test'
        self.api_key: str = '123456789'
        self.client: TimeseriesClient = TimeseriesClient(
            domain=self.domain,
            api_key=self.api_key
        )

    @responses.activate
    def test_get_timeseries_data(self) -> None:
        mock_response: TimeseriesResponse = {
            'timeseries': [
                {
                    'node_id': 1,
                    'tag': 'outdoortemp',
                    'data': [
                        {
                            'v': 2.6,
                            'ts': '2020-01-01T00:05:57+01:00'
                        },
                        {
                            'v': 2.6,
                            'ts': '2020-01-01T00:15:37+01:00'
                        }
                    ]
                }
            ]
        }

        responses.add(
            responses.GET,
            url=f'{self.client._url}/{self.client._timeseries_api_path}',
            json=mock_response,
            status=200
        )

        with self.subTest('call successful with complete parameter list'):
            params: Dict[str, Any] = {
                'node_id': 1,
                'node_ids': [1, 2],
                'tag': 'outdoortemp',
                'tags': ['outdoortemp, indoortemp'],
                'start': '2020-01-01T00:05:57+01:00',
                'end': '2020-01-01T00:05:57+01:00',
                'resolution': 'second',
                'aggregate': 'avg',
                'epoch': True,
            }

            res: TimeseriesResponse = self.client.get_timeseries_data(**params)

            self.assertEqual(res, mock_response)
            self.assertEqual(len(responses.calls), 1)

            expected_query_params: Dict[str, Any] = {
                **params,
                'node_id': str(params['node_id']),
                'node_ids': json.dumps(params['node_ids']),
                'tags': json.dumps(params['tags']),
                'epoch': '1',
            }

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._timeseries_api_path}'
                f'?{urllib.parse.urlencode(expected_query_params)}'
            )
            self.assertEqual(responses.calls[0].request.params.get('node_id'), expected_query_params['node_id'])
            self.assertEqual(responses.calls[0].request.params.get('node_ids'), expected_query_params['node_ids'])
            self.assertEqual(responses.calls[0].request.params.get('tag'), expected_query_params['tag'])
            self.assertEqual(responses.calls[0].request.params.get('tags'), expected_query_params['tags'])
            self.assertEqual(responses.calls[0].request.params.get('start'), expected_query_params['start'])
            self.assertEqual(responses.calls[0].request.params.get('end'), expected_query_params['end'])
            self.assertEqual(responses.calls[0].request.params.get('resolution'), expected_query_params['resolution'])
            self.assertEqual(responses.calls[0].request.params.get('aggregate'), expected_query_params['aggregate'])
            self.assertEqual(responses.calls[0].request.params.get('epoch'), expected_query_params['epoch'])

    @responses.activate
    def test_store_timeseries_data(self) -> None:
        mock_response: TimeseriesDataResponse = {
            'node_id': 1,
            'tag': 'outdoortemp',
            'value': 13.4,
            'ts': '2019-10-01T11:30:22+02'
        }

        responses.add(
            responses.POST,
            url=f'{self.client._url}/{self.client._timeseries_api_path}',
            json=mock_response,
            status=200
        )

        with self.subTest('call successful with complete parameter list'):
            body: Dict[str, Any] = {
                'node_id': 1,
                'tag': 'outdoortemp',
                'val': 13.4,
                'ts': '2019-10-01T11:30:22+02'
            }

            res: TimeseriesDataResponse = self.client.store_timeseries_data(**body)

            self.assertEqual(res, mock_response)
            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._timeseries_api_path}'
            )
            body_params: Dict[str, str] = urllib.parse.parse_qs(responses.calls[0].request.body)
            self.assertEqual(body_params['node_id'][0], str(body['node_id']))
            self.assertEqual(body_params['tag'][0], body['tag'])
            self.assertEqual(body_params['val'][0], str(body['val']))
            self.assertEqual(body_params['ts'][0], body['ts'])

    @responses.activate
    def test_store_multiple_timeseries_data(self) -> None:
        timeseries: TimeseriesType = {
            'node_id': 1,
            'tag': 'outdoortemp',
            'data': [
                {
                    'v': 2.6,
                    'ts': '2020-01-01T00:05:57+01:00'
                },
                {
                    'v': 2.6,
                    'ts': '2020-01-01T00:15:37+01:00'
                }
            ]
        }

        mock_response: TimeseriesResponse = {
            'timeseries': [timeseries]
        }

        responses.add(
            responses.POST,
            url=f'{self.client._url}/{self.client._timeseries_api_path}',
            json=mock_response,
            status=200
        )

        with self.subTest('call successful with complete parameter list'):
            body: Dict[str, Any] = {
                'timeseries': [timeseries],
                'overwrite': 'replace_window',
                'silent': True,
            }

            res: Optional[TimeseriesResponse] = self.client.store_multiple_timeseries_data(**body)

            self.assertEqual(res, mock_response)
            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._timeseries_api_path}'
            )
            body_params: Dict[str, str] = urllib.parse.parse_qs(responses.calls[0].request.body)
            self.assertEqual(body_params['timeseries'][0], json.dumps(body['timeseries']))
            self.assertEqual(body_params['overwrite'][0], body['overwrite'])
            self.assertEqual(body_params['silent'][0], str(body['silent']))
