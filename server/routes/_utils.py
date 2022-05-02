"""Utility functions for the routing submodule."""

import json
import os
import pathlib
from typing import TypeVar

__all__ = [
    'static_from_json'
]

T = TypeVar('T')


def static_from_json(cls: type[T], filename: str) -> dict[int, T]:
    """Return static data from a local JSON file.

    Args:
        cls (Any): The dataclass type to instantiate
        filename (str): The filename to instantate `cls` from

    Returns:
        dict[int, Any]: A mapping of IDs to data classes.

    """
    data_dir = os.path.join(pathlib.Path(__file__).parents[2], 'data')
    with open(os.path.join(data_dir, filename), encoding='utf-8') as _data:
        return {d['id']: cls(**d) for d in json.load(_data)}
