"""Custom types used by the API host module.

This includes basic data classes.
"""

import dataclasses
from typing import Generic, TypeVar

_T = TypeVar('_T')


@dataclasses.dataclass(frozen=True)
class FactionData(Generic[_T]):
    """Container for faction-specific data."""

    vs: _T
    nc: _T
    tr: _T
    nso: _T


@dataclasses.dataclass(frozen=True)
class OutfitInfo:
    """Container for outfit data."""

    outfit_id: int
    name: str
    tag: str
