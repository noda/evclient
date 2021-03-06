from warnings import filterwarnings
from typing import Dict, Optional

import requests
from beartype import beartype
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

from .base_client import BaseClient
from .utils import filter_none_values_from_dict

filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
Response = requests.models.Response


class SettingsClient(BaseClient):
    """
    A client for handling the settings / metadata section of EnergyView API.
    """

    @beartype
    def __init__(self,
                 domain: Optional[str] = None,
                 api_key: Optional[str] = None,
                 endpoint_url: Optional[str] = None
                 ) -> None:
        super().__init__(domain, api_key, endpoint_url)
        self._settings_api_path: str = 'settings'

    @beartype
    def get_settings(self,
                     settings_type: str,
                     settings_id: int,
                     path: Optional[str] = None,
                     extract: Optional[bool] = False
                     ) -> Dict:
        """Fetches all settings / metadata of a resource from EnergyView API

        Args:
            settings_type (str): One of:

               - cluster

               - node

               - report

               - netmgr

            settings_id (int): The numeric id associated with the resource.
            path (Optional[str]): Filter using the specified path. Separator is '.' (dot). For example: coco.default.
            extract (Optional[bool]): Unique identifier for the integration. When set to True,
                everything beneath path will be extracted and returned. For example::

                    extract=False and path=coco.default
                    Result:
                    {"coco": {"default": {"hello": "world"}}}
                    Compared to:
                    extract=True and path=coco.default
                    Result:
                    {"hello": "world"}

                    Or:
                    extract=True and path=coco.default.hello
                    Result:
                    "world"

        Returns:
            Dict of settings, keys will vary depending on the settings_type and resource requested

        Raises:
            :class:`.EVUnexpectedStatusCodeException`: Unexpected status code received.
            :class:`.EVBadRequestException`: Sent request had insufficient data or invalid options.
            :class:`.EVUnauthorizedException`: Request was refused due to lacking authentication credentials.
            :class:`.EVForbiddenException`: Server understands the request but refuses to authorize it.
            :class:`.EVNotFoundException`: The requested resource was not found.
            :class:`.EVTooManyRequestsException`: Sent too many requests in a given amount of time.
            :class:`.EVInternalServerException`: Server encountered an unexpected condition that prevented it
                from fulfilling the request.
        """
        response: Response = self._session.get(
            url=f'{self._url}/{self._settings_api_path}/{settings_type}/{settings_id}',
            params=filter_none_values_from_dict({
                'path': path,
                'extract': 1 if extract else 0
            })
        )
        return self._process_response(response)

    @beartype
    def store_settings(self,
                       settings_type: str,
                       settings_id: int,
                       path: str,
                       value: str,
                       force: Optional[bool] = False
                       ) -> Dict[str, str]:
        """Store a value in settings / metadata of a resource from EnergyView API

        Args:
            settings_type (str): One of:

                - cluster

                - node

                - report

                - netmgr

            settings_id (int): The numeric id associated with the resource.
            path (str): Target path. Separator is '.' (dot). For example: coco.default.
            value (str): Any JSON compatible value. Objects are not supported and will be converted to string.
            force (Optional[bool]): Force the new value to be written. Even if the type
                (boolean, string, integer, float) is different from the old value.

        Returns:
            Dict[str, str] that will contain the value provided.

        Raises:
            :class:`.EVUnexpectedStatusCodeException`: Unexpected status code received.
            :class:`.EVBadRequestException`: Sent request had insufficient data or invalid options.
            :class:`.EVUnauthorizedException`: Request was refused due to lacking authentication credentials.
            :class:`.EVForbiddenException`: Server understands the request but refuses to authorize it.
            :class:`.EVNotFoundException`: The requested resource was not found.
            :class:`.EVTooManyRequestsException`: Sent too many requests in a given amount of time.
            :class:`.EVInternalServerException`: Server encountered an unexpected condition that prevented it
                from fulfilling the request.
        """
        response: Response = self._session.put(
            url=f'{self._url}/{self._settings_api_path}/{settings_type}/{settings_id}',
            data=filter_none_values_from_dict({
                'path': path,
                'value': value,
                'force': 1 if force else None
            })
        )
        return self._process_response(response)
