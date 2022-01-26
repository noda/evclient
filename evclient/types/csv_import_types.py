from typing import List

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict


class CSVImportIntegrationType(TypedDict):
    """
    Attributes:
        uuid: Unique identifier for the integration.
        title: Name of the integration.
    """
    uuid: str
    title: str


class CSVImportResponse(TypedDict):
    """
    Attributes:
        integrations: Named wrapper attribute.
    """
    integrations: List[CSVImportIntegrationType]
