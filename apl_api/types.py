"""Custom types used by the API host module.

This includes basic data classes.
"""

from typing import Generic, NewType, TypeVar

import pydantic

_T = TypeVar('_T')


BaseId = NewType('BaseId', int)
BaseTypeId = NewType('BaseTypeId', int)
ContinentId = NewType('ContinentID', int)
FactionId = NewType('FactionId', int)
OutfitId = NewType('OutfitId', int)
ResourceId = NewType('ResourceId', int)
ServerId = NewType('ServerId', int)
OutfitTag = NewType('OutfitTag', str)


class FactionData(Generic[_T], pydantic.BaseModel):
    """Generic container for faction-specific data."""

    vs: _T
    nc: _T
    tr: _T
    nso: _T
