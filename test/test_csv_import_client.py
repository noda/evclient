import os
import responses
import unittest

from typing import TextIO

from evclient import CSVImportClient, CSVImportResponseType


class TestCSVImportClient(unittest.TestCase):
    def setUp(self) -> None:
        self.domain: str = 'test'
        self.api_key: str = '123456789'
        self.client: CSVImportClient = CSVImportClient(
            domain=self.domain,
            api_key=self.api_key
        )

        self.file: TextIO = open('testfile.csv', 'w+')

    def tearDown(self) -> None:
        self.file.close()
        os.remove('testfile.csv')

    @responses.activate
    def test_get_csv_imports(self) -> None:
        mock_response: CSVImportResponseType = {
            'integrations': [
                {
                    'uuid': '945978fd-bd61-4d83-a1e4-02ef89d60987',
                    'title': 'My CSV importer'
                },
                {
                    'uuid': '53a13531-6430-4014-8155-f8d05df12e68',
                    'title': 'Price forecast importer'
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

            res: CSVImportResponseType = self.client.get_csv_imports()

            self.assertEqual(res, mock_response)
            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._api_path}'
            )

    @responses.activate
    def test_upload_csv_file(self) -> None:
        import_uuid = '82a4d745-ba1b-4683-af05-b100e1e637a3'
        with self.subTest('call successful with complete parameter list'):
            responses.add(
                responses.POST,
                url=f'{self.client._url}/{self.client._api_path}/{import_uuid}',
                status=200
            )

            self.client.upload_csv_file(import_uuid, self.file)

            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._api_path}/{import_uuid}',
            )
            self.assertIn('testfile.csv', responses.calls[0].request.body.decode('utf-8'))
