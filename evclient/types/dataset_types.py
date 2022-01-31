from typing import List, Optional

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict


class DatasetType(TypedDict):
    """
    Attributes:
        uuid: This is the unique identifier for this particular data set.
        name: The name (human readable) of the data set.
        format: The format of the stored content.
        checksum: The SHA256 checksum of the content.
        size: The size of the (decoded) content in bytes.
        thing_uuid: The optional reference to a Node/Thing. If not used this value will be null.
        created: The timestamp (RFC 3339, section 5.6) when this object was created.
        updated: The timestamp (RFC 3339, section 5.6) when this object was last update.
        created_by: A reference to the account ID (user) who created it the data set.
        updated_by: A reference to thge account ID (user) who performed the last update of the data set.
        tags: An optional list of tags used for filtering and identification. If not used the result is an empty list []
    """
    uuid: str
    name: str
    format: str
    checksum: str
    size: int
    thing_uuid: Optional[str]
    created: str
    updated: str
    created_by: int
    updated_by: int
    tags: List[str]
