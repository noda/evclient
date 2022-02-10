import json
import datetime
from warnings import filterwarnings
from typing import List, Optional, Union

import requests
import pyrfc3339
from beartype import beartype
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

from .types.timeseries_types import (
    TimeseriesResponseGroup,
    TimeseriesResponse,
    StoreTimeseriesResponse,
    TimeseriesGroup,
    TimeseriesResponseData,
    TimeseriesData,
    StoreTimeseriesData
)
from .base_client import BaseClient
from .utils import filter_none_values_from_dict

filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
Response = requests.models.Response


class TimeseriesClient(BaseClient):
    """
    A client for handling the timeseries section of EnergyView API.
    """

    @beartype
    def __init__(self,
                 domain: Optional[str] = None,
                 api_key: Optional[str] = None,
                 endpoint_url: Optional[str] = None
                 ) -> None:
        super().__init__(domain, api_key, endpoint_url)
        self._timeseries_api_path: str = 'timeseries'

    @beartype
    def get_timeseries_data(self,
                            node_ids: Optional[Union[int, List[int]]] = None,
                            tags: Optional[Union[str, List[str]]] = None,
                            start: Optional[datetime.datetime] = None,
                            end: Optional[datetime.datetime] = None,
                            resolution: Optional[str] = None,
                            aggregate: Optional[str] = None,
                            epoch: Optional[bool] = False
                            ) -> List[TimeseriesGroup]:
        """Fetches all timeseries data from EnergyView API

        Args:
            node_ids (Optional[Union[int,List[int]]]): Filter on one or several unique node identifiers.
            tags (Optional[Union[str,List[str]]]): Filter on one or several sensor names.
            start (Optional[datetime.datetime]): The from date-time of the query window.
                Without timezone information, the API will fall back to the time zone configured for the domain.
                Defaults to now.
            end (Optional[datetime.datetime]): The from date-time of the query window.
                Without timezone information, the API will fall back to the time zone configured for the domain.
                Defaults to now.
            resolution (Optional[str]): Truncates all timestamps to any of (options),
                then computes the average for all points within the truncated period.

                -   second

                -   minute

                -   5minute

                -   10minute

                -   15minute

                -   20minute

                -   30minute

                -   hour

                -   day

                -   month

                -   year

                -   decade

                -   century

                -   millennia

            aggregate (Optional[str]): When using resolution, select this aggregate function
                instead of the default avg when computing the result.

                -   avg

                -   min

                -   max

                -   sum

                -   count

            epoch (Optional[bool]): When set to True, the ts field will be in Unix timestamp format (numeric)
                instead of a string. This is the number of seconds that have elapsed since the Unix epoch,
                which is the time 00:00:00 UTC on 1 January 1970.

        Returns:
            List[:class:`.TimeseriesGroup`]

        Raises:
            :class:`.EVUnexpectedStatusCodeException`: Unexpected status code received.
            :class:`.EVBadRequestException`: Sent request had insufficient data or invalid options.
            :class:`.EVUnauthorizedException`: Request was refused due to lacking authentication credentials.
            :class:`.EVForbiddenException`: Server understands the request but refuses to authorize it.
            :class:`.EVTooManyRequestsException`: Sent too many requests in a given amount of time.
            :class:`.EVInternalServerException`: Server encountered an unexpected condition that prevented it
                from fulfilling the request.
        """

        def parse_row(row: TimeseriesResponseData) -> TimeseriesData:
            return {
                'ts': pyrfc3339.parse(row.get('ts')),
                'v': row.get('v')
            }

        node_id = None
        if isinstance(node_ids, int):
            node_id = node_ids
            node_ids = None

        tag = None
        if isinstance(tags, str):
            tag = tags
            tags = None

        response: Response = self._session.get(
            url=f'{self._url}/{self._timeseries_api_path}',
            params=filter_none_values_from_dict({
                'node_id': node_id,
                'node_ids': json.dumps(node_ids) if node_ids else None,
                'tag': tag,
                'tags': json.dumps(tags) if tags else None,
                'start': start.isoformat() if start is not None else None,
                'end': end.isoformat() if end is not None else None,
                'resolution': resolution,
                'aggregate': aggregate,
                'epoch': 1 if epoch else None,
            })
        )

        r: TimeseriesResponse = self._process_response(response)
        if r is None:
            return []

        timeseries: List[TimeseriesResponseGroup] = r.get('timeseries', [])
        if timeseries is not None:
            timeseries: List[TimeseriesGroup] = [{
                'node_id': obj.get('node_id'),
                "tag": obj.get('tag'),
                'data': [parse_row(row) for row in obj.get('data', [])]
            } for obj in timeseries]
        return timeseries

    @beartype
    def store_timeseries_data(self,
                              node_id: int,
                              tag: str,
                              val: float,
                              ts: datetime.datetime,
                              silent: Optional[bool] = True
                              ) -> Optional[StoreTimeseriesData]:
        """Store a single data point in a timeseries from EnergyView API

        Args:
            node_id (int): Domain-unique id for the node.
            tag (str): The name of the tag / sensor as declared in EnergyView. Such as outdoortemp, indoortemp etc.
            val (float): The value to store.
            ts (datetime): The date time of the data point in the format YYYY-MM-DDThh:mm:ss±hh:mm.
                Without timezone information, the API will fall back to the time zone configured for the domain.
            silent (Optional[bool]): Return None instead of the inserted content.

        Returns:
            :class:`.StoreTimeseriesData` or None depending on if the `silent` param is set.

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
            url=f'{self._url}/{self._timeseries_api_path}',
            data=filter_none_values_from_dict({
                'node_id': node_id,
                'tag': tag,
                'val': val,
                'ts': ts.isoformat() if ts is not None else None,
                'silent': 'true' if silent else None
            })
        )
        if silent:
            return None
        response_data: StoreTimeseriesResponse = self._process_response(response)
        return {
            'node_id': response_data['node_id'],
            'tag': response_data['tag'],
            'value': response_data['value'],
            'ts': pyrfc3339.parse(response_data['ts'])
        }

    @beartype
    def store_multiple_timeseries_data(self,
                                       timeseries: List[TimeseriesGroup],
                                       overwrite: Optional[bool] = False,
                                       silent: Optional[bool] = True,
                                       ) -> Optional[List[TimeseriesGroup]]:
        """Store multiple data points in multiple timeseries from EnergyView API

        Args:
            timeseries (List[TimeseriesGroup]): A list of timeseries objects::

                [
                    {
                        'node_id': 1,
                        'tag': 'outdoortemp',
                        'data': [{
                            'v': 2.6,
                            'ts': datetime.datetime(2020, 1, 1, 0, 0, tzinfo=<UTC+01:00>)
                        },{
                            'v': 2.6,
                            'ts': datetime.datetime(2020, 1, 1, 0, 15, tzinfo=<UTC+01:00>)
                        }]
                    }
                ]

            overwrite (Optional[bool]): Deletes all datapoints between the lowest and highest ts (a >= x AND a <= y),
                for each node_id and corresponding tag. Then inserts all the new datapoints.
            silent (Optional[bool]): When set to true a call will only reply with status code 201 Created and an empty
                reply instead of 200 Success and the inserted rows. Defaults to True.

        Returns:
            List[:class:`.TimeseriesGroup`] or None depending on if the `silent` param is set.

        Raises:
            :class:`.EVUnexpectedStatusCodeException`: Unexpected status code received.
            :class:`.EVBadRequestException`: Sent request had insufficient data or invalid options.
            :class:`.EVUnauthorizedException`: Request was refused due to lacking authentication credentials.
            :class:`.EVForbiddenException`: Server understands the request but refuses to authorize it.
            :class:`.EVTooManyRequestsException`: Sent too many requests in a given amount of time.
            :class:`.EVInternalServerException`: Server encountered an unexpected condition that prevented it
                from fulfilling the request.
        """

        def parse_row(row: TimeseriesResponseData) -> TimeseriesData:
            return {
                'ts': pyrfc3339.parse(row.get('ts')),
                'v': row.get('v')
            }

        response: Response = self._session.post(
            url=f'{self._url}/{self._timeseries_api_path}',
            data=filter_none_values_from_dict({
                'timeseries': json.dumps(timeseries),
                'overwrite': "replace_window" if overwrite is True else None,
                'silent': 'true' if silent else None
            })
        )

        r: TimeseriesResponse = self._process_response(response)
        if r is None or silent:
            return None

        timeseries: List[TimeseriesResponseGroup] = r.get('timeseries')
        if timeseries is not None:
            timeseries: List[TimeseriesGroup] = [{
                'node_id': obj.get('node_id'),
                'tag': obj.get('tag'),
                'data': [parse_row(row) for row in obj.get('data', [])]
            } for obj in timeseries]
        return timeseries
