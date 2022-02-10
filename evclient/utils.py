from typing import Dict
from warnings import filterwarnings

from beartype import beartype
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)


@beartype
def filter_none_values_from_dict(target) -> Dict:
    return {k: v for k, v in target.items() if v is not None}
