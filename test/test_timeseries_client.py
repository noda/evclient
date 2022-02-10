import copy
import json
from typing import Dict, Any, Optional, List

import pyrfc3339
import responses
import unittest
import urllib


from evclient import (
    TimeseriesClient,
    TimeseriesResponse,
    StoreTimeseriesResponse,
    TimeseriesResponseGroup,
    TimeseriesGroup,
    StoreTimeseriesData
)


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

        def parse_response(response: TimeseriesResponse) -> List[TimeseriesGroup]:
            return [{
                'node_id': obj.get('node_id'),
                'tag': obj.get('tag'),
                'data': [
                    {
                        'ts': pyrfc3339.parse(row.get('ts')),
                        'v': row.get('v')
                    } for row in obj.get("data", [])
                ]
            } for obj in response.get('timeseries', [])]

        with self.subTest('call successful with multiple node_ids and tags in the parameter list'):
            params: Dict[str, Any] = {
                'node_ids': [1, 2],
                'tags': ['outdoortemp, indoortemp'],
                'start': pyrfc3339.parse('2020-01-01T00:05:57+01:00'),
                'end': pyrfc3339.parse('2020-01-01T00:05:57+01:00'),
                'resolution': 'second',
                'aggregate': 'avg',
                'epoch': True,
            }

            res: List[TimeseriesGroup] = self.client.get_timeseries_data(**params)

            self.assertEqual(res, parse_response(mock_response))
            self.assertEqual(len(responses.calls), 1)

            expected_query_params: Dict[str, Any] = {
                **params,
                'start': params['start'].isoformat(),
                'end': params['end'].isoformat(),
                'node_ids': json.dumps(params['node_ids']),
                'tags': json.dumps(params['tags']),
                'epoch': '1',
            }
            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._timeseries_api_path}'
                f'?{urllib.parse.urlencode(expected_query_params)}'
            )
            self.assertEqual(responses.calls[0].request.params.get('node_id'), None)
            self.assertEqual(responses.calls[0].request.params.get('node_ids'), expected_query_params['node_ids'])
            self.assertEqual(responses.calls[0].request.params.get('tag'), None)
            self.assertEqual(responses.calls[0].request.params.get('tags'), expected_query_params['tags'])
            self.assertEqual(responses.calls[0].request.params.get('start'), expected_query_params['start'])
            self.assertEqual(responses.calls[0].request.params.get('end'), expected_query_params['end'])
            self.assertEqual(responses.calls[0].request.params.get('resolution'), expected_query_params['resolution'])
            self.assertEqual(responses.calls[0].request.params.get('aggregate'), expected_query_params['aggregate'])
            self.assertEqual(responses.calls[0].request.params.get('epoch'), expected_query_params['epoch'])

        with self.subTest('call successful with a single node_id and tag in the parameter list'):
            params: Dict[str, Any] = {
                'node_ids': 1,
                'tags': 'indoortemp',
                'start': pyrfc3339.parse('2020-01-01T00:05:57+01:00'),
                'end': pyrfc3339.parse('2020-01-01T00:05:57+01:00'),
                'resolution': 'second',
                'aggregate': 'avg',
                'epoch': True,
            }

            res: List[TimeseriesGroup] = self.client.get_timeseries_data(**params)

            self.assertEqual(res, parse_response(mock_response))
            self.assertEqual(len(responses.calls), 2)

            expected_query_params: Dict[str, Any] = {
                'node_id': str(params['node_ids']),
                'tag': params['tags'],
                'start': params['start'].isoformat(),
                'end': params['end'].isoformat(),
                'resolution': params['resolution'],
                'aggregate': params['aggregate'],
                'epoch': '1',
            }
            expected_query_string: Dict[str, Any] = copy.deepcopy(expected_query_params)

            self.assertEqual(
                responses.calls[1].request.url,
                f'{self.client._url}/{self.client._timeseries_api_path}'
                f'?{urllib.parse.urlencode(expected_query_string)}'
            )

            self.assertEqual(responses.calls[1].request.params.get('node_id'), expected_query_params['node_id'])
            self.assertEqual(responses.calls[1].request.params.get('node_ids'), None)
            self.assertEqual(responses.calls[1].request.params.get('tag'), expected_query_params['tag'])
            self.assertEqual(responses.calls[1].request.params.get('tags'), None)
            self.assertEqual(responses.calls[1].request.params.get('start'), expected_query_params['start'])
            self.assertEqual(responses.calls[1].request.params.get('end'), expected_query_params['end'])
            self.assertEqual(responses.calls[1].request.params.get('resolution'), expected_query_params['resolution'])
            self.assertEqual(responses.calls[1].request.params.get('aggregate'), expected_query_params['aggregate'])
            self.assertEqual(responses.calls[1].request.params.get('epoch'), expected_query_params['epoch'])

    @responses.activate
    def test_store_timeseries_data(self) -> None:
        mock_response: StoreTimeseriesResponse = {
            'node_id': 1,
            'tag': 'outdoortemp',
            'value': 13.4,
            'ts': '2019-10-01T11:30:22+02:00'
        }

        responses.add(
            responses.POST,
            url=f'{self.client._url}/{self.client._timeseries_api_path}',
            json=mock_response,
            status=200
        )

        def parse_response(obj):
            return {
                'node_id': obj.get('node_id'),
                'tag': obj.get('tag'),
                'value': obj.get('value'),
                'ts': pyrfc3339.parse(obj.get('ts'))
            }

        with self.subTest('call successful with complete parameter list'):
            body: Dict[str, Any] = {
                'node_id': 1,
                'tag': 'outdoortemp',
                'val': 13.4,
                'ts': pyrfc3339.parse('2019-10-01T11:30:22+02:00'),
                'silent': False
            }

            res: Optional[StoreTimeseriesData] = self.client.store_timeseries_data(**body)

            self.assertEqual(res, parse_response(mock_response))
            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._timeseries_api_path}'
            )
            body_params: Dict[str, str] = urllib.parse.parse_qs(responses.calls[0].request.body)
            self.assertEqual(body_params['node_id'][0], str(body['node_id']))
            self.assertEqual(body_params['tag'][0], body['tag'])
            self.assertEqual(body_params['val'][0], str(body['val']))
            self.assertEqual(pyrfc3339.parse(body_params['ts'][0]), body['ts'])

    @responses.activate
    def test_store_multiple_timeseries_data(self) -> None:
        timeseries: TimeseriesResponseGroup = {
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

        def parse_response(response: TimeseriesResponse) -> List[TimeseriesGroup]:
            return [{
                'node_id': obj.get('node_id'),
                'tag': obj.get('tag'),
                'data': [
                    {
                        'ts': pyrfc3339.parse(row.get('ts')),
                        'v': row.get('v')
                    } for row in obj.get("data", [])
                ]
            } for obj in response.get('timeseries', [])]

        with self.subTest('call successful with complete parameter list'):
            body: Dict[str, Any] = {
                'timeseries': [timeseries],
                'overwrite': True,
                'silent': False,
            }

            res: Optional[TimeseriesResponse] = self.client.store_multiple_timeseries_data(**body)

            self.assertEqual(res, parse_response(mock_response))
            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._timeseries_api_path}'
            )
            body_params: Dict[str, str] = urllib.parse.parse_qs(responses.calls[0].request.body)

            self.assertEqual(body_params['timeseries'][0], json.dumps(body['timeseries']))
            self.assertEqual(body_params['overwrite'][0], 'replace_window' if body.get('overwrite') is True else None)
