import json.decoder
import os
import logging
from warnings import filterwarnings
from typing import Type, Dict, Optional, Any

import yaml
import requests
from beartype import beartype
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

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
    EVUnexpectedStatusCodeException,
)

filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
logger = logging.getLogger(__name__)
Response = requests.models.Response


class BaseClient:
    """
    A base class for clients that should make requests to EnergyView API

    Should only be used as an abstract class.
    """

    responses: Dict[int, Type[Exception]] = {
        400: EVBadRequestException,
        401: EVUnauthorizedException,
        402: EVRequestFailedException,
        403: EVForbiddenException,
        404: EVNotFoundException,
        409: EVConflictException,
        429: EVTooManyRequestsException,
    }

    @beartype
    def __init__(self,
                 domain: Optional[str] = None,
                 api_key: Optional[str] = None,
                 endpoint_url: Optional[str] = None
                 ) -> None:
        """BaseClient constructor

        Defines the base url and customer domain for the EnergyView API and sets headers in a new
        requests session.

        Will look for the following environment variables if parameters are omitted:

        EV_DOMAIN

        EV_API_KEY

        EV_ENDPOINT_URL

        Args:
            domain (Optional[str]): The EnergyView domain to make requests to.
            api_key (Optional[str]): API Key for the selected EnergyView domain.
            endpoint_url (Optional[str]): Alternative EnergyView URL

        Raises:
            :class:`.EVFatalErrorException`: The client could not find a specified domain
                or api key for the EnergyView API
        """
        if endpoint_url:
            self._base_url: str = endpoint_url
        elif os.environ.get('EV_ENDPOINT_URL'):
            self._base_url: str = os.environ.get('EV_ENDPOINT_URL')
        else:
            self._base_url: str = 'https://customer.noda.se'

        self._api_root: str = 'api'
        self._api_version: str = 'v1'

        if domain:
            self._domain = domain
        elif os.environ.get('EV_DOMAIN'):
            self._domain = os.environ.get('EV_DOMAIN')
        else:
            raise EVFatalErrorException('No domain provided to EVClient')

        self._session = requests.Session()
        self._session.headers = {'Accept': 'application/json'}
        if api_key:
            self._session.headers['Authorization'] = f'Key {api_key}'
        elif os.environ.get('EV_API_KEY'):
            self._session.headers['Authorization'] = f'Key {os.environ.get("EV_API_KEY")}'
        else:
            raise EVFatalErrorException('No api key provided to EVClient')

        self._url: str = f'{self._base_url}/{self._domain}/{self._api_root}/{self._api_version}'

    @beartype
    def _handle_successful_response(self, response: Response) -> Optional[Any]:
        if response.headers.get('content-type') == 'application/yaml':
            try:
                return yaml.safe_load(response.text)
            except yaml.YAMLError:
                return response.content or None
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return response.content or None

    @beartype
    def _process_response(self, response: Response) -> Optional[Any]:
        """Process the response from EnergyView API

        Returns:
            Will return the json encoded content if there is any content, else None will be returned.

        Args:
            response: requests.model.Response object

        Raises:
            :class:`.EVUnexpectedStatusCodeException`: Unexpected status code received.
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

        if response.status_code < 400:
            return self._handle_successful_response(response)
        elif 400 <= response.status_code < 500:
            msg = None
            try:
                if response.headers.get("content-type") == "application/json":
                    msg = response.json().get("error")
            except json.decoder.JSONDecodeError:
                pass
            exception = self.responses.get(response.status_code, EVUnexpectedStatusCodeException)
            raise exception(msg)
        else:
            raise EVInternalServerException
