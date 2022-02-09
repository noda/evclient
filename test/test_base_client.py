import json
import os
from typing import TextIO

import requests
import responses
import unittest
import yaml

from evclient import BaseClient
from evclient import (
    EVBadRequestException,
    EVUnauthorizedException,
    EVRequestFailedException,
    EVForbiddenException,
    EVNotFoundException,
    EVConflictException,
    EVTooManyRequestsException,
    EVInternalServerException,
    EVFatalErrorException
)

Response = requests.models.Response


class TestBaseClient(unittest.TestCase):
    def setUp(self) -> None:
        self.domain: str = 'test'
        self.api_key: str = '123456789'

        self.file: TextIO = open('testfile.yaml', 'w+')
        yaml.dump({'header': []}, self.file, default_flow_style=False, allow_unicode=True)
        self.file.close()

    def tearDown(self) -> None:
        self.file.close()
        os.remove('testfile.yaml')

    def test_credentials_from_input_params(self) -> None:
        client: BaseClient = BaseClient(
            domain=self.domain,
            api_key=self.api_key
        )
        self.assertEqual(client._domain, self.domain)
        self.assertEqual(client._session.headers, {
            'Authorization': f'Key {self.api_key}',
            'Accept': 'application/json'
        })

    @unittest.mock.patch.dict(os.environ, {
        'EV_DOMAIN': 'test',
        'EV_API_KEY': '123456789',
    })
    def test_credentials_from_env_vars(self) -> None:
        client: BaseClient = BaseClient()
        self.assertEqual(client._domain, 'test')
        self.assertEqual(client._session.headers, {
            'Authorization': 'Key 123456789',
            'Accept': 'application/json'
        })

    @unittest.mock.patch.dict(os.environ, {
        'EV_DOMAIN': 'test',
    })
    def test_credentials_from_env_vars_no_api_key(self) -> None:
        self.assertRaises(EVFatalErrorException, BaseClient)

    @unittest.mock.patch.dict(os.environ, {
        'EV_API_KEY': '123456789',
    })
    def test_credentials_from_env_vars_no_domain(self) -> None:
        self.assertRaises(EVFatalErrorException, BaseClient)

    @responses.activate
    def test_request_auth_header_is_set(self) -> None:
        """
        Makes a mocked request and makes sure that the Authorization header is set correctly by.
        """
        client: BaseClient = BaseClient(
            domain=self.domain,
            api_key=self.api_key
        )

        responses.add(
            responses.GET,
            url=client._base_url,
            json={},
            status=200
        )
        client._session.get(client._base_url)

        self.assertEqual(responses.calls[0].request.headers.get('Authorization'), f'Key {self.api_key}')

    @responses.activate
    def test_handle_successful_response(self) -> None:
        client: BaseClient = BaseClient(
            domain=self.domain,
            api_key=self.api_key
        )

        with self.subTest('Returns parsed yaml'):
            with open(self.file.name) as file:
                file_content = yaml.safe_load(file)
                responses.add(
                    responses.GET,
                    url=client._base_url,
                    body=json.dumps(file_content).encode('utf-8'),
                    content_type='application/yaml',
                    status=200
                )
                response: Response = requests.get(client._base_url)
                self.assertEqual(client._handle_successful_response(response), file_content)

        with self.subTest('Returns None'):
            responses.add(
                responses.GET,
                url=client._base_url,
                status=200
            )
            response: Response = requests.get(client._base_url)
            self.assertEqual(client._handle_successful_response(response), None)

        with self.subTest('Returns content in bytes'):
            responses.add(
                responses.GET,
                url=client._base_url,
                body='not json, but valid body',
                status=200
            )
            response: Response = requests.get(client._base_url)
            self.assertEqual(client._handle_successful_response(response).decode('utf-8'), 'not json, but valid body')

        with self.subTest('Returns valid json'):
            responses.add(
                responses.GET,
                url=client._base_url,
                json={},
                status=200
            )
            response: Response = requests.get(client._base_url)
            self.assertEqual(client._handle_successful_response(response), {})

    @responses.activate
    def test_process_response(self) -> None:
        client: BaseClient = BaseClient(
            domain=self.domain,
            api_key=self.api_key
        )

        with self.subTest('Returns parsed yaml'):
            with open(self.file.name) as file:
                file_content = yaml.safe_load(file)
                responses.add(
                    responses.GET,
                    url=client._base_url,
                    body=json.dumps(file_content).encode('utf-8'),
                    content_type='application/yaml',
                    status=200
                )
                response: Response = requests.get(client._base_url)
                self.assertEqual(client._handle_successful_response(response), file_content)

        with self.subTest('OK status code and returns valid json'):
            responses.add(
                responses.GET,
                url=client._base_url,
                json={},
                status=200
            )
            response: Response = requests.get(client._base_url)
            self.assertEqual(client._process_response(response), {})

        with self.subTest('OK status code and returns None'):
            responses.add(
                responses.GET,
                url=client._base_url,
                status=200
            )
            response: Response = requests.get(client._base_url)
            self.assertEqual(client._process_response(response), None)

        with self.subTest('OK status code and returns content in bytes'):
            responses.add(
                responses.GET,
                url=client._base_url,
                body='not json, but valid body',
                status=200
            )
            response: Response = requests.get(client._base_url)
            self.assertEqual(client._process_response(response).decode('utf-8'), 'not json, but valid body')

        with self.subTest('Should raise PCTBadRequestException'):
            responses.add(responses.GET, url=client._base_url, status=400)
            response: Response = requests.get(client._base_url)
            self.assertRaises(EVBadRequestException, client._process_response, response)

        with self.subTest('Should raise PCTUnauthorizedException'):
            responses.add(responses.GET, url=client._base_url, status=401)
            response = requests.get(client._base_url)
            self.assertRaises(EVUnauthorizedException, client._process_response, response)

        with self.subTest('Should raise PCTForbiddenException'):
            responses.add(responses.GET, url=client._base_url, status=403)
            response: Response = requests.get(client._base_url)
            self.assertRaises(EVForbiddenException, client._process_response, response)

        with self.subTest('Should raise PCTNotFoundException'):
            responses.add(responses.GET, url=client._base_url, status=404)
            response: Response = requests.get(client._base_url)
            self.assertRaises(EVNotFoundException, client._process_response, response)

        with self.subTest('Should raise EVRequestFailedException'):
            responses.add(responses.GET, url=client._base_url, status=402)
            response: Response = requests.get(client._base_url)
            self.assertRaises(EVRequestFailedException, client._process_response, response)

        with self.subTest('Should raise PCTConflictException'):
            responses.add(responses.GET, url=client._base_url, status=409)
            response: Response = requests.get(client._base_url)
            self.assertRaises(EVConflictException, client._process_response, response)

        with self.subTest('Should raise PCTTooManyRequestsException'):
            responses.add(responses.GET, url=client._base_url, status=429)
            response: Response = requests.get(client._base_url)
            self.assertRaises(EVTooManyRequestsException, client._process_response, response)

        with self.subTest('Should raise PCTInternalServerException'):
            responses.add(responses.GET, url=client._base_url, status=500)
            response: Response = requests.get(client._base_url)
            self.assertRaises(EVInternalServerException, client._process_response, response)

        with self.subTest('request is logged successfully'):
            responses.add(
                responses.GET,
                url=client._base_url,
                body='Example body',
                status=200
            )

            with self.assertLogs('evclient', level='DEBUG') as cm:
                response: Response = requests.get(client._base_url)
                client._process_response(response)
                self.assertEqual(cm.output[0], (
                    'DEBUG:evclient.base_client:'
                    'API Request sent:\n'
                    f'Url: {response.request.url}\n'
                    f'Body: {response.request.body}\n'
                    f'Status Code: {response.status_code}'
                ))
