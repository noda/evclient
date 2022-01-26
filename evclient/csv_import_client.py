import requests
from typing import TextIO

from .types.csv_import_types import CSVImportResponse
from .base_client import BaseClient

Response = requests.models.Response


class CSVImportClient(BaseClient):
    """
    A client for handling the csv import section of EnergyView API.
    """

    def __init__(self, domain: str = None, api_key: str = None):
        super().__init__(domain, api_key)
        self._api_path: str = 'csvimport'

    def get_csv_imports(self) -> CSVImportResponse:
        """Fetches all existing csv import definitions from EnergyView API

        Returns:
            :class:`.CSVImportResponse`

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

    def upload_csv_file(self, import_uuid: str, csv_file: TextIO) -> None:
        """Upload a CSV file to the EnergyView API

        Args:
            import_uuid (str): The id of the csv import integration.
            csv_file (TextIO): The file to upload.

        Raises:
            :class:`.EVBadRequestException`: Sent request had insufficient data or invalid options.
            :class:`.EVUnauthorizedException`: Request was refused due to lacking authentication credentials.
            :class:`.EVForbiddenException`: Server understands the request but refuses to authorize it.
            :class:`.EVNotFoundException`: The requested resource was not found.
            :class:`.EVTooManyRequestsException`: Sent too many requests in a given amount of time.
            :class:`.EVInternalServerException`: Server encountered an unexpected condition that prevented it
                                        from fulfilling the request.
        """
        response: Response = self._session.post(
            url=f'{self._url}/{self._api_path}/{import_uuid}',
            files={'file': csv_file}
        )
        return self._process_response(response)
