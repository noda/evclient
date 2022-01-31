from .csv_import_client import CSVImportClient
from .node_client import NodeClient
from .tag_client import TagClient
from .settings_client import SettingsClient
from .timeseries_client import TimeseriesClient
from .dataset_client import DatasetClient


class EVClient(
    CSVImportClient,
    NodeClient,
    TagClient,
    SettingsClient,
    TimeseriesClient,
    DatasetClient
):
    """
    A class for handling all sections of NODA EnergyView API combined into one client
    """
    pass
