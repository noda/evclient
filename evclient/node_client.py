import requests

from .types.node_types import NodeResponse
from .base_client import BaseClient

Response = requests.models.Response


class NodeClient(BaseClient):
    """
    A client for handling the node / collectors section of EnergyView API.
    """

    def __init__(self, domain: str = None, api_key: str = None, endpoint_url: str = None):
        super().__init__(domain, api_key, endpoint_url)
        self._api_path: str = 'nodes'

    def get_nodes(self) -> NodeResponse:
        """Fetches all nodes / collectors from EnergyView API

        Returns:
            :class:`.NodeResponse`

        Raises:
            :class:`.EVBadRequestException`: Sent request had insufficient data or invalid options.
            :class:`.EVUnauthorizedException`: Request was refused due to lacking authentication credentials.
            :class:`.EVForbiddenException`: Server understands the request but refuses to authorize it.
            :class:`.EVTooManyRequestsException`: Sent too many requests in a given amount of time.
            :class:`.EVInternalServerException`: Server encountered an unexpected condition that prevented it
                                        from fulfilling the request.
        """
        response: Response = self._session.get(
            url=f'{self._url}/{self._api_path}'
        )
        return self._process_response(response)
