from warnings import filterwarnings
from typing import List, Any, Optional

import requests
from beartype import beartype
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

from .types.dataset_types import DatasetType
from .base_client import BaseClient
from .utils import filter_none_values_from_dict

filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
Response = requests.models.Response


class DatasetClient(BaseClient):
    """
    A client for handling the dataset section of EnergyView API.
    """

    @beartype
    def __init__(self,
                 domain: Optional[str] = None,
                 api_key: Optional[str] = None,
                 endpoint_url: Optional[str] = None
                 ) -> None:
        super().__init__(domain, api_key, endpoint_url)
        self._dataset_api_path: str = 'dataset'

    @beartype
    def get_datasets(self,
                     offset: Optional[int] = None,
                     limit: Optional[int] = None
                     ) -> List[DatasetType]:
        """Fetches datasets from EnergyView API

        Args:
            offset (Optional[int]): An integer with the lowest value of 0. Used to skew (offset) the result range.
            limit (Optional[int]): An integer with the lowest value of 1 and the highest value of 100.
                Used to limit the amount of results returned for each "page".

        Returns:
            List[:class:`.DatasetType`]

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
            url=f'{self._url}/{self._dataset_api_path}',
            params=filter_none_values_from_dict({
                'offset': offset,
                'limit': limit
            })
        )
        return self._process_response(response)

    @beartype
    def create_dataset(self,
                       content: str,
                       dataset_format: str,
                       name: str,
                       tags: Optional[List[str]] = None,
                       thing_uuid: Optional[str] = None
                       ) -> DatasetType:
        """Create a dataset in EnergyView API

        Args:
            content (str): The base64 encoded content of the object/file.
            dataset_format (str): One of csv, ini, json, misc, toml, xml, yaml.
            name (str): Name of the data set object.
            tags (Optional[List[str]]): Optional element used for filtering and identification. A list/array of strings.
            thing_uuid (Optional[str]): Optional element used to bind a data set to a Node/Thing.
                Uses the globally unique identifier (UUID) of a Node/Thing.

        Returns:
            :class:`.DatasetType`

        Raises:
            :class:`.EVUnexpectedStatusCodeException`: Unexpected status code received.
            :class:`.EVBadRequestException`: Sent request had insufficient data or invalid options.
            :class:`.EVUnauthorizedException`: Request was refused due to lacking authentication credentials.
            :class:`.EVForbiddenException`: Server understands the request but refuses to authorize it.
            :class:`.EVTooManyRequestsException`: Sent too many requests in a given amount of time.
            :class:`.EVInternalServerException`: Server encountered an unexpected condition that prevented it
                from fulfilling the request.
        """
        response: Response = self._session.post(
            url=f'{self._url}/{self._dataset_api_path}',
            json=filter_none_values_from_dict({
                'content': content,
                'format': dataset_format,
                'name': name,
                'tags': tags,
                'thing_uuid': thing_uuid
            })
        )
        return self._process_response(response)

    @beartype
    def get_dataset(self, dataset_uuid: str) -> DatasetType:
        """Fetches a specific dataset from EnergyView API by uuid

        Args:
            dataset_uuid (str): The UUID of the data set.

        Returns:
            :class:`.DatasetType`

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
            url=f'{self._url}/{self._dataset_api_path}/{dataset_uuid}'
        )
        return self._process_response(response)

    @beartype
    def get_dataset_content(self, dataset_uuid: str) -> Any:
        """Fetches the raw content of a specific dataset from EnergyView API

        Args:
            dataset_uuid (str): The UUID of the data set.

        Returns:
            Will return different results depending on the format of the raw content retrieved.

            The Content-Type header will be one of::

                text/csv: csv
                text/plan; charset=utf-8: ini
                application/json: json
                application/toml: toml
                application/xml: xml
                application/yaml: yaml
                application/octet-stream: misc

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
            url=f'{self._url}/{self._dataset_api_path}/{dataset_uuid}/raw'
        )
        return self._process_response(response)

    @beartype
    def update_dataset(self,
                       dataset_uuid: str,
                       content: Optional[str] = None,
                       dataset_format: Optional[str] = None,
                       name: Optional[str] = None,
                       tags: Optional[List[str]] = None,
                       thing_uuid: Optional[str] = None
                       ) -> None:
        """Update a dataset in EnergyView API

        Args:
            dataset_uuid (str): The UUID of the data set.
            content (Optional[str]): The base64 encoded content of the object/file.
            dataset_format (Optional[str]): One of csv, ini, json, misc, toml, xml, yaml.
            name (Optional[str]): Name of the data set object.
            tags (Optional[List[str]]): Optional element used for filtering and identification. A list/array of strings.
            thing_uuid (Optional[str]): Optional element used to bind a data set to a Node/Thing.
                Uses the globally unique identifier (UUID) of a Node/Thing.

        Raises:
            :class:`.EVUnexpectedStatusCodeException`: Unexpected status code received.
            :class:`.EVBadRequestException`: Sent request had insufficient data or invalid options.
            :class:`.EVUnauthorizedException`: Request was refused due to lacking authentication credentials.
            :class:`.EVForbiddenException`: Server understands the request but refuses to authorize it.
            :class:`.EVTooManyRequestsException`: Sent too many requests in a given amount of time.
            :class:`.EVInternalServerException`: Server encountered an unexpected condition that prevented it
                from fulfilling the request.
        """
        response: Response = self._session.put(
            url=f'{self._url}/{self._dataset_api_path}/{dataset_uuid}',
            json=filter_none_values_from_dict({
                'content': content,
                'format': dataset_format,
                'name': name,
                'tags': tags,
                'thing_uuid': thing_uuid
            })
        )
        return self._process_response(response)

    @beartype
    def delete_dataset(self, dataset_uuid: str) -> None:
        """Deletes a specific dataset from EnergyView API by uuid

        Args:
            dataset_uuid (str): The UUID of the data set.

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
        response: Response = self._session.delete(
            url=f'{self._url}/{self._dataset_api_path}/{dataset_uuid}'
        )
        return self._process_response(response)
