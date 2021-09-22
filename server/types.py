"""Custom types used by the API host module.

This includes basic data classes.
"""

from typing import NewType

from pydantic import BaseModel, Field


BaseId = NewType('BaseId', int)
BaseTypeId = NewType('BaseTypeId', int)
ContinentId = NewType('ContinentID', int)
FactionId = NewType('FactionId', int)
OutfitId = NewType('OutfitId', int)
ResourceId = NewType('ResourceId', int)
ServerId = NewType('ServerId', int)
OutfitTag = NewType('OutfitTag', str)


class Population(BaseModel):
    """Population estimates mapped by faction identifier."""

    vs: int = Field(
        title='VS',
        description='Estimated Vanu Sovereignty population',
        example=31)
    nc: int = Field(
        title='NC',
        description='Estimated New Conglomerate population',
        example=11)
    tr: int = Field(
        title='TR',
        description='Estimated Terran Republic population',
        example=26)
    nso: int = Field(
        title='NSO',
        description='Estimated Nanite Systems Operatives population',
        example=4)
