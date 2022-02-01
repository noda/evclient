import json.decoder
import os
import logging
from typing import Type, Dict, Optional, Any

import requests

from .exceptions import (
    EVBadRequestException,
    EVUnauthorizedException,
    EVRequestFailedException,
    EVForbiddenException,
    EVNotFoundException,
    EVConflictException,
    EVTooManyRequestsException,
    EVInternalServerException,
    EVFatalErrorException,
)

logger = logging.getLogger(__name__)
Response = requests.models.Response


class BaseClient:
    """
    A base class for clients that should make requests to EnergyView API

    Should only be used as an abstract class.
    """

    def __init__(self, domain: str = None, api_key: str = None) -> None:
        """BaseClient constructor

        Defines the base url and customer domain for the EnergyView API and sets headers in a new
        requests session.

        Will look for the following environment variables if parameters are omitted:

        EV_DOMAIN

        EV_API_KEY

        Args:
            domain (Optional[str]): The EnergyView domain to make requests to.
            api_key (Optional[str]): API Key for the selected EnergyView domain.

        Raises:
            :class:`.EVFatalErrorException`: The client could not find a specified domain
                or api key for the EnergyView API
        """
        self._base_url: str = 'https://customer.noda.se'
        self._api_root: str = 'api'
        self._api_version: str = 'v1'
        self._url: str = f'{self._base_url}/{self._api_root}/{self._api_version}'
        if domain:
            self._domain = domain
        elif os.environ.get('EV_DOMAIN'):
            self._domain = os.environ.get('EV_DOMAIN')
        else:
            raise EVFatalErrorException('No domain provided to EVCClient')

        self._session = requests.Session()
        self._session.headers = {'Accept': 'application/json'}
        if api_key:
            self._session.headers['Authorization'] = f'Bearer {api_key}'
        elif os.environ.get('EV_API_KEY'):
            self._session.headers['Authorization'] = f'Bearer {os.environ.get("EV_API_KEY")}'
        else:
            raise EVFatalErrorException('No api key provided to EVCClient')

    def _process_response(self, response: Response) -> Optional[Any]:
        """Process the response from EnergyView API

        Returns:
            Will return the json encoded content if there is any content, else None will be returned.

        Args:
            response: requests.model.Response object

        Raises:
            :class:`.EVBadRequestException`: Sent request had insufficient data or invalid options.
            :class:`.EVUnauthorizedException`: Request was refused due to lacking authentication credentials.
            :class:`.EVRequestFailedException`: The parameters were valid but the request failed.
            :class:`.EVForbiddenException`: Server understands the request but refuses to authorize it.
            :class:`.EVNotFoundException`: The requested resource was not found.
            :class:`.EVConflictException`: The request conflicts with the current state of the target resource.
            :class:`.EVTooManyRequestsException`: Sent too many requests in a given amount of time.
            :class:`.EVInternalServerException`: Server encountered an unexpected condition that prevented it
                                        from fulfilling the request.
        """
        logger.debug(
            f'API Request sent:\n'
            f'Url: {response.request.url}\n'
            f'Body: {response.request.body}\n'
            f'Status Code: {response.status_code}'
        )
        responses: Dict[int, Type[Exception]] = {
            400: EVBadRequestException,
            401: EVUnauthorizedException,
            402: EVRequestFailedException,
            403: EVForbiddenException,
            404: EVNotFoundException,
            409: EVConflictException,
            429: EVTooManyRequestsException,
        }
        if response.status_code < 400:
            try:
                return response.json()
            except json.decoder.JSONDecodeError:
                return response.content or None
        elif 400 <= response.status_code < 500:
            raise responses[response.status_code]
        else:
            raise EVInternalServerException
