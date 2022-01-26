from typing import List

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict


class DeviceType(TypedDict):
    """
    Attributes:
        id: Id of the Device.
        name: Name of the Device.
        protocol_id: Protocol id of the Device.
    """
    id: int
    name: str
    protocol_id: int


class NodeType(TypedDict):
    """
    Attributes:
        id: Domain-unique id of the Node.
        uuid: An UUIDv4 ID which should be unique across domains. Since id is only unique on a singe domain.
        name: Human readable name of the Node.
        description: Human readable description of the Node.
        public: Boolean to declare if this node is public to all accounts in the domain.
        owner: Boolean to show if the account performing the request is the owner of the Node or not.
        enabled: State used by several different component to determine of the Node should be used.
        archived: An alternative to deleting the node and loosing everything.
        representation: Machine centrict purpose declaration of the Node. Used by different component of the system.
        device: Legacy purpose declaration of the Node. Required as it a central part of the design.
            A device is a sub-set of a Protocol.
        sensor_ids: A list of sensor id attached to this Node.
        interval: A period in seconds of how often data is expected to be stored on the Node.
            Used by the alert system to determine faults.
    """
    id: int
    uuid: str
    name: str
    description: str
    public: bool
    owner: bool
    enabled: bool
    archived: bool
    representation: str
    device: DeviceType
    sensor_ids: List[int]
    interval: int


class NodeResponse(TypedDict):
    """
    Attributes:
        nodes: Named wrapper attribute
    """
    nodes: List[NodeType]
