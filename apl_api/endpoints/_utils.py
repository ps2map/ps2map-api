import json
import os
import pathlib
from typing import Dict, List, Type, TypeVar

from fastapi.params import Query

__all__ = [
    'IdListQuery',
    'id_from_string'
]

_DataT = TypeVar('_DataT')

# Validator for comma-separated ID lists (positive integers only)
IdListQuery = Query('', regex='^\\d+(,\\d+)*$')


def ids_from_string(string: str) -> List[int]:
    """Return a list of integers from a comma-separated string.

    Empty substrings between commas are ignored.

    Args:
        string (str): The string to split. May be empty.

    Returns:
        List[int]: A list of integers in the string.

    """
    return [int(s) for s in string.split(',') if s]


def static_from_json(cls: Type[_DataT], filename: str) -> Dict[int, _DataT]:
    """Return static data from a local JSON file.

    Args:
        cls (Type[Any]): The dataclass type to instantiate
        filename (str): The filename to instantate `cls` from

    Returns:
        Dict[int, Any]: A mapping of IDs to data classes.

    """
    data_dir = os.path.join(pathlib.Path(__file__).parents[2], 'tests', 'data')
    with open(os.path.join(data_dir, filename)) as _data:
        return {d['id']: cls(**d) for d in json.load(_data)}
