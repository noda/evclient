from typing import List
import datetime

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

    
class TimeseriesResponseData(TypedDict):
    """
    Attributes:
        v: Value of the data point.
        ts: Date time string on the format YYYY-MM-DDThh:mm:ss±hh:mm.
    """
    v: float
    ts: str


class TimeseriesResponseGroup(TypedDict):
    """
    Attributes:
        node_id: Domain-unique identifier for the node.
        tag: Name of the sensor for which the data belongs.
        data: A list (array) of data points as object.
    """
    node_id: int
    tag: str
    data: List[TimeseriesResponseData]


class TimeseriesResponse(TypedDict):
    """
    Attributes:
        timeseries: Named wrapper attribute
    """
    timeseries: List[TimeseriesResponseGroup]


class TimeseriesDataResponse(TypedDict):
    """
    Attributes:
        node_id: Domain-unique id for the node.
        tag: The name of the tag / sensor as declared in EnergyView.
        v: Value of the data point.
        ts: Date time string on the format YYYY-MM-DDThh:mm:ss±hh:mm.
    """
    node_id: int
    tag: str
    value: float
    ts: str


class TimeseriesData(TypedDict):
    """
    Attributes:
        v: Value of the data point.
        ts: Date time object
    """
    v: float
    ts: datetime.datetime

    
class TimeseriesGroup(TypedDict):
    """
    Attributes:
        node_id: Domain-unique identifier for the node.
        tag: Name of the sensor for which the data belongs.
        data: A list (array) of data points as object.        
    """
    node_id: int
    tag: str
    data: List[TimeseriesData]

class TimeseriesElements(List[TimeseriesGroup]):
    pass
