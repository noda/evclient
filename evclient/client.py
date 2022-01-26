from .csv_import_client import CSVImportClient
from .node_client import NodeClient
from .tag_client import TagClient


class EVClient(
    CSVImportClient,
    NodeClient,
    TagClient
):
    """
    A class for handling all sections of NODA EnergyView API combined into one client
    """
    pass
