from warnings import filterwarnings
from typing import List, Optional

import requests
from beartype import beartype
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

from .types.node_types import NodeType, NodeResponse
from .base_client import BaseClient

filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
Response = requests.models.Response


class NodeClient(BaseClient):
    """
    A client for handling the node / collectors section of EnergyView API.
    """

    @beartype
    def __init__(self,
                 domain: Optional[str] = None,
                 api_key: Optional[str] = None,
                 endpoint_url: Optional[str] = None
                 ) -> None:
        super().__init__(domain, api_key, endpoint_url)
        self._node_api_path: str = 'nodes'

    @beartype
    def get_nodes(self) -> List[NodeType]:
        """Fetches all nodes / collectors from EnergyView API

        Returns:
            List[:class:`.NodeType`]

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
            url=f'{self._url}/{self._node_api_path}'
        )
        response_data: NodeResponse = self._process_response(response)
        return [] if response_data is None else response_data.get('nodes')
