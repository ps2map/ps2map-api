"""Custom types used by the API host module.

This includes basic data classes.
"""

import dataclasses
from typing import Generic, NewType, TypeVar

_T = TypeVar('_T')


BaseId = NewType('BaseId', int)
BaseTypeId = NewType('BaseTypeId', int)
ContinentId = NewType('ContinentID', int)
FactionId = NewType('FactionId', int)
OutfitId = NewType('OutfitId', int)
ResourceId = NewType('ResourceId', int)
ServerId = NewType('ServerId', int)
OutfitTag = NewType('OutfitTag', str)


@dataclasses.dataclass(frozen=True)
class FactionData(Generic[_T]):
    """Generic container for faction-specific data."""

    vs: _T
    nc: _T
    tr: _T
    nso: _T
