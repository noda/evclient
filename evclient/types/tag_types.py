from typing import List

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict


class TagType(TypedDict):
    """
    Attributes:
        id: Domain-unique id of the sensor. A sensor (declaration) is usually assigned to multiple nodes.
            In a domain with thousands of Nodes there may only still be less then a hundred sensors.
        name: Declared name of the sensor, used throughout the system. Only unique in combination with protocol_id.
        description: Human readable declaration of the sensor.
        postfix: May serve as the unit.
        protocol_id: Reference to a protocol. A protocol is a set of sensors acting as a declaration of ability.
    """
    id: int
    name: str
    description: str
    postfix: str
    protocol_id: int


class TagResponse(TypedDict):
    """
    Attributes:
        sensors: Named wrapper attribute
    """
    sensors: List[TagType]
