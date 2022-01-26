from typing import List

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict


class CSVImportIntegrationType(TypedDict):
    uuid: str
    title: str


class CSVImportResponseType(TypedDict):
    integrations: List[CSVImportIntegrationType]
