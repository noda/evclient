import csv
import json
import os

import responses
import unittest
import urllib
from typing import Dict, List, Union, Any, TextIO

from evclient import DatasetClient, DatasetType


class TestDatasetClient(unittest.TestCase):
    def setUp(self) -> None:
        self.domain: str = 'test'
        self.api_key: str = '123456789'
        self.client: DatasetClient = DatasetClient(
            domain=self.domain,
            api_key=self.api_key
        )

        self.file: TextIO = open('testfile.csv', 'w+')
        writer = csv.writer(self.file)
        writer.writerow(['Column1', 'Column2', 'Column3'])
        self.file.close()

    def tearDown(self) -> None:
        self.file.close()
        os.remove('testfile.csv')

    @responses.activate
    def test_get_datasets(self) -> None:
        mock_response: List[DatasetType] = [
            {
                'uuid': '11eff124-fdd1-4b0e-9d1a-52b9fe8497cb',
                'name': 'Dataset #1',
                'format': 'yaml',
                'size': 41,
                'checksum': 'eb488679e0c0de6ac2e8446be252767b18fedea0c0a404b9bf12a530ca79c199',
                'thing_uuid': None,
                'created': '2021-10-01 12:26:26.42555+02',
                'created_by': 1,
                'updated': '2021-10-04 09:30:28+02',
                'updated_by': 1,
                'tags': []
            }
        ]

        responses.add(
            responses.GET,
            url=f'{self.client._url}/{self.client._api_path}',
            json=mock_response,
            status=200
        )

        with self.subTest('call successful with complete parameter list'):
            params: Dict[str, int] = {
                'offset': 1,
                'limit': 1
            }

            res: List[DatasetType] = self.client.get_datasets(**params)

            self.assertEqual(res, mock_response)
            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._api_path}'
                f'?{urllib.parse.urlencode(params)}'
            )
            self.assertEqual(responses.calls[0].request.params.get('offset'), str(params['offset']))
            self.assertEqual(responses.calls[0].request.params.get('limit'), str(params['limit']))

    @responses.activate
    def test_create_dataset(self) -> None:
        mock_response: DatasetType = {
            'uuid': '11eff124-fdd1-4b0e-9d1a-52b9fe8497cb',
            'name': 'Dataset #1',
            'format': 'yaml',
            'size': 41,
            'checksum': 'eb488679e0c0de6ac2e8446be252767b18fedea0c0a404b9bf12a530ca79c199',
            'thing_uuid': None,
            'created': '2021-10-01 12:26:26.42555+02',
            'created_by': 1,
            'updated': '2021-10-04 09:30:28+02',
            'updated_by': 1,
            'tags': []
        }

        responses.add(
            responses.POST,
            url=f'{self.client._url}/{self.client._api_path}',
            json=mock_response,
            status=200
        )

        with self.subTest('call successful with complete parameter list'):
            params: Dict[str, Union[int, List[str]]] = {
                'content': 'R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA ==',
                'dataset_format': 'yaml',
                'name': 'Dataset #1',
                'tags': ['tag1'],
                'thing_uuid': '22eff124-fdd1-4b0e-9d1a-52b9fe8497cb',
            }

            res: DatasetType = self.client.create_dataset(**params)

            self.assertEqual(res, mock_response)
            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._api_path}'
            )
            parsed_request_body: Any = json.loads(responses.calls[0].request.body.decode('utf-8'))
            self.assertEqual(parsed_request_body['content'], params['content'])
            self.assertEqual(parsed_request_body['format'], params['dataset_format'])
            self.assertEqual(parsed_request_body['name'], params['name'])
            self.assertEqual(parsed_request_body['tags'], params['tags'])
            self.assertEqual(parsed_request_body['thing_uuid'], params['thing_uuid'])

    @responses.activate
    def test_get_dataset(self) -> None:
        mock_response: DatasetType = {
            'uuid': '11eff124-fdd1-4b0e-9d1a-52b9fe8497cb',
            'name': 'Dataset #1',
            'format': 'yaml',
            'size': 41,
            'checksum': 'eb488679e0c0de6ac2e8446be252767b18fedea0c0a404b9bf12a530ca79c199',
            'thing_uuid': None,
            'created': '2021-10-01 12:26:26.42555+02',
            'created_by': 1,
            'updated': '2021-10-04 09:30:28+02',
            'updated_by': 1,
            'tags': []
        }

        dataset_uuid = '11eff124-fdd1-4b0e-9d1a-52b9fe8497cb'

        responses.add(
            responses.GET,
            url=f'{self.client._url}/{self.client._api_path}/{dataset_uuid}',
            json=mock_response,
            status=200
        )

        with self.subTest('call successful with complete parameter list'):

            res: DatasetType = self.client.get_dataset(dataset_uuid)

            self.assertEqual(res, mock_response)
            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._api_path}/{dataset_uuid}'
            )

    @responses.activate
    def test_get_dataset_content(self) -> None:
        dataset_uuid = '11eff124-fdd1-4b0e-9d1a-52b9fe8497cb'
        with open(self.file.name) as file:
            file_content = file.read()
            responses.add(
                responses.GET,
                url=f'{self.client._url}/{self.client._api_path}/{dataset_uuid}/raw',
                body=file_content,
                content_type='text/csv',
                status=200
            )

            with self.subTest('call successful with complete parameter list'):
                res: bytes = self.client.get_dataset_content(dataset_uuid)

                self.assertEqual(res.decode('utf-8'), file_content)
                self.assertEqual(len(responses.calls), 1)

                self.assertEqual(
                    responses.calls[0].request.url,
                    f'{self.client._url}/{self.client._api_path}/{dataset_uuid}/raw'
                )

    @responses.activate
    def test_update_dataset(self) -> None:
        dataset_uuid = '11eff124-fdd1-4b0e-9d1a-52b9fe8497cb'
        responses.add(
            responses.PUT,
            url=f'{self.client._url}/{self.client._api_path}/{dataset_uuid}',
            status=200
        )

        with self.subTest('call successful with complete parameter list'):
            params: Dict[str, Union[int, List[str]]] = {
                'content': 'R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA ==',
                'dataset_format': 'yaml',
                'name': 'Dataset #1',
                'tags': ['tag1'],
                'thing_uuid': '22eff124-fdd1-4b0e-9d1a-52b9fe8497cb',
            }

            self.client.update_dataset(dataset_uuid, **params)

            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._api_path}/{dataset_uuid}'
            )
            parsed_request_body: Any = json.loads(responses.calls[0].request.body.decode('utf-8'))
            self.assertEqual(parsed_request_body['content'], params['content'])
            self.assertEqual(parsed_request_body['format'], params['dataset_format'])
            self.assertEqual(parsed_request_body['name'], params['name'])
            self.assertEqual(parsed_request_body['tags'], params['tags'])
            self.assertEqual(parsed_request_body['thing_uuid'], params['thing_uuid'])

    @responses.activate
    def test_delete_dataset(self) -> None:
        dataset_uuid = '11eff124-fdd1-4b0e-9d1a-52b9fe8497cb'

        responses.add(
            responses.DELETE,
            url=f'{self.client._url}/{self.client._api_path}/{dataset_uuid}',
            status=200
        )

        with self.subTest('call successful with complete parameter list'):
            self.client.delete_dataset(dataset_uuid)

            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._api_path}/{dataset_uuid}'
            )
