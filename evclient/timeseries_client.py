import pyrfc3339
import json
from typing import List, Optional

import requests

from .types.timeseries_types import (
    TimeseriesResponseData,
    TimeseriesResponseGroup,
    TimeseriesResponse,
    TimeseriesDataResponse,
    TimeseriesData,
    TimeseriesGroup,
    TimeseriesElements
)
from .base_client import BaseClient
from .utils import filter_none_values_from_dict

Response = requests.models.Response


class TimeseriesClient(BaseClient):
    """
    A client for handling the timeseries section of EnergyView API.
    """

    def __init__(self, domain: str = None, api_key: str = None, endpoint_url: str = None):
        super().__init__(domain, api_key, endpoint_url)
        self._timeseries_api_path: str = 'timeseries'

    def get_timeseries_data(self,
                            node_id: int = None,
                            node_ids: List[int] = None,
                            tag: str = None,
                            tags: List[str] = None,
                            start: str = None,
                            end: str = None,
                            resolution: str = None,
                            aggregate: str = None,
                            epoch: bool = False
                            ) -> TimeseriesElements:
        """Fetches all timeseries data from EnergyView API

        Args:
            node_id (Optional[int]): Filter on the unique identifier for a specific node.
            node_ids (Optional[List[int]]): Filter on several unique node identifiers.
                Can not be used together with node_id.
            tag (Optional[str]): Filter on a sensor name.
            tags (Optional[List[str]]): Filter on several sensor names. Can not be used together with tag.
            start (Optional[str]): The from date time string on the format YYYY-MM-DDThh:mm:ss±hh:mm.
                Without timezone information, the API will fall back to the time zone configured for the domain.
                Defaults to now.
            end (Optional[str]): The from date time string on the format YYYY-MM-DDThh:mm:ss±hh:mm.
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
            :class:`.TimeseriesElements`

        Raises:
            :class:`.EVBadRequestException`: Sent request had insufficient data or invalid options.
            :class:`.EVUnauthorizedException`: Request was refused due to lacking authentication credentials.
            :class:`.EVForbiddenException`: Server understands the request but refuses to authorize it.
            :class:`.EVTooManyRequestsException`: Sent too many requests in a given amount of time.
            :class:`.EVInternalServerException`: Server encountered an unexpected condition that prevented it
                                        from fulfilling the request.
        """
        response: Response = self._session.get(
            url=f'{self._url}/{self._timeseries_api_path}',
            params=filter_none_values_from_dict({
                'node_id': node_id,
                'node_ids': json.dumps(node_ids) if node_ids else None,
                'tag': tag,
                'tags': json.dumps(tags) if tags else None,
                'start': start,
                'end': end,
                'resolution': resolution,
                'aggregate': aggregate,
                'epoch': 1 if epoch else None,
            })
        )

        def parse_row(x):
            return {
                "ts": pyrfc3339.parse(x.get("ts")),
                "v": x.get("v")
            }

        r: TimeseriesResponse = self._process_response(response)
        if r is None:
            return None

        timeseries: List[TimeseriesResponseGroup] = r.get("timeseries")
        if timeseries is not None:
            timeseries = [{
                "node_id": obj.get("node_id"),
                "tag": obj.get("tag"),
                "data": [parse_row(row) for row in obj.get("data", [])]
            } for obj in timeseries]
        return timeseries

    def store_timeseries_data(self,
                              node_id: int,
                              tag: str,
                              val: float,
                              ts: str,
                              silent: bool = True
                              ) -> Optional[TimeseriesDataResponse]:
        """Store a single data point in a timeseries from EnergyView API

        Args:
            node_id (int): Domain-unique id for the node.
            tag (str): The name of the tag / sensor as declared in EnergyView. Such as outdoortemp, indoortemp etc.
            val (float): The value to store.
            ts (str): The date time of the data point as string on the format YYYY-MM-DDThh:mm:ss±hh:mm.
                Without timezone information, the API will fall back to the time zone configured for the domain.
            silent (bool): Reply with 201 and an empty body instead of the inserted content.

        Returns:
            :class:`.TimeseriesDataResponse` or None depending on if the `silent` param is set.

        Raises:
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
                'ts': ts,
                'silent': 'true' if silent else None
            })
        )
        return self._process_response(response)

    def store_multiple_timeseries_data(self,
                                       timeseries: List[TimeseriesGroup],
                                       overwrite: str = None,
                                       silent: bool = True,
                                       ) -> Optional[TimeseriesElements]:
        """Store multiple data points in multiple timeseries from EnergyView API

        Args:
            timeseries (List[TimeseriesType]): A list of timeseries objects::

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

            overwrite (Optional[str]): Possible values are:

                - replace_window

                replace_window first deletes all datapoints between the lowest and highest ts (a >= x AND a <= y),
                for each node_id and corresponding tag. Then inserts all the new datapoints.
            silent (Optional[bool]): When set to true a call will only reply with status code 201 Created and an empty
                reply instead of 200 Success and the inserted rows. Defaults to True.

        Returns:
            :class:`.TimeseriesElements` or None depending on if the `silent` param is set.

        Raises:
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
                'timeseries': json.dumps(timeseries),
                'overwrite': overwrite,
                'silent': 'true' if silent else None
            })
        )
        return self._process_response(response)
