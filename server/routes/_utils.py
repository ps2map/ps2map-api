import json
import os
import pathlib
from typing import Dict, Type, TypeVar

__all__ = [
    'static_from_json'
]

_DataT = TypeVar('_DataT')


def static_from_json(cls: Type[_DataT], filename: str) -> Dict[int, _DataT]:
    """Return static data from a local JSON file.

    Args:
        cls (Type[Any]): The dataclass type to instantiate
        filename (str): The filename to instantate `cls` from

    Returns:
        Dict[int, Any]: A mapping of IDs to data classes.

    """
    data_dir = os.path.join(pathlib.Path(__file__).parents[2], 'data')
    with open(os.path.join(data_dir, filename)) as _data:
        return {d['id']: cls(**d) for d in json.load(_data)}
