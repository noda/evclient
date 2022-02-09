from typing import List

import responses
import unittest

from evclient import TagClient, TagResponse, TagType


class TestTagClient(unittest.TestCase):
    def setUp(self) -> None:
        self.domain: str = 'test'
        self.api_key: str = '123456789'
        self.client: TagClient = TagClient(
            domain=self.domain,
            api_key=self.api_key
        )

    @responses.activate
    def test_get_tags(self) -> None:
        mock_response: TagResponse = {
            'sensors': [
                {
                    'id': 1,
                    'name': 'outdoortemp',
                    'description': 'Outdoor temperature sensor',
                    'postfix': 'C',
                    'protocol_id': 1
                }
            ]
        }
        with self.subTest('call successful with complete parameter list'):
            responses.add(
                responses.GET,
                url=f'{self.client._url}/{self.client._tag_api_path}',
                json=mock_response,
                status=200
            )

            res: List[TagType] = self.client.get_tags()

            self.assertEqual(res, mock_response.get('sensors'))
            self.assertEqual(len(responses.calls), 1)

            self.assertEqual(
                responses.calls[0].request.url,
                f'{self.client._url}/{self.client._tag_api_path}'
            )
