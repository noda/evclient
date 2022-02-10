from warnings import filterwarnings
from typing import List, Optional

import requests
from beartype import beartype
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

from .types.tag_types import TagResponse, TagType
from .base_client import BaseClient

filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
Response = requests.models.Response


class TagClient(BaseClient):
    """
    A client for handling the tag / sensor section of EnergyView API.
    """

    @beartype
    def __init__(self,
                 domain: Optional[str] = None,
                 api_key: Optional[str] = None,
                 endpoint_url: Optional[str] = None
                 ) -> None:
        super().__init__(domain, api_key, endpoint_url)
        self._tag_api_path: str = 'tags'

    @beartype
    def get_tags(self) -> List[TagType]:
        """Fetches all tags / sensors from EnergyView API

        Returns:
            List[:class:`.TagType`]

        Raises:
            :class:`.EVUnexpectedStatusCodeException`: Unexpected status code received.
            :class:`.EVBadRequestException`: Sent request had insufficient data or invalid options.
            :class:`.EVUnauthorizedException`: Request was refused due to lacking authentication credentials.
            :class:`.EVForbiddenException`: Server understands the request but refuses to authorize it.
            :class:`.EVTooManyRequestsException`: Sent too many requests in a given amount of time.
            :class:`.EVInternalServerException`: Server encountered an unexpected condition that prevented it
                from fulfilling the request.
        """
        response: Response = self._session.get(
            url=f'{self._url}/{self._tag_api_path}'
        )
        response_data: TagResponse = self._process_response(response)
        return [] if response_data is None else response_data.get('sensors')
