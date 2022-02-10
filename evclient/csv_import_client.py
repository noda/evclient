from warnings import filterwarnings
from typing import TextIO, Optional

import requests
from beartype import beartype
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

from .types.csv_import_types import CSVImportResponse
from .base_client import BaseClient


filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
Response = requests.models.Response


class CSVImportClient(BaseClient):
    """
    A client for handling the csv import section of EnergyView API.
    """

    @beartype
    def __init__(self,
                 domain: Optional[str] = None,
                 api_key: Optional[str] = None,
                 endpoint_url: Optional[str] = None
                 ) -> None:
        super().__init__(domain, api_key, endpoint_url)
        self._csv_import_api_path: str = 'csvimport'

    @beartype
    def get_csv_imports(self) -> CSVImportResponse:
        """Fetches all existing csv import definitions from EnergyView API

        Returns:
            :class:`.CSVImportResponse`

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
            url=f'{self._url}/{self._csv_import_api_path}'
        )
        return self._process_response(response)

    def upload_csv_file(self, import_uuid: str, csv_file: TextIO) -> None:
        """Upload a CSV file to the EnergyView API

        Args:
            import_uuid (str): The id of the csv import integration.
            csv_file (TextIO): The file to upload.

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
        response: Response = self._session.post(
            url=f'{self._url}/{self._csv_import_api_path}/{import_uuid}',
            files={'file': csv_file}
        )
        return self._process_response(response)
