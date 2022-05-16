"""Dataclass representations of payloads sent between the DB and API.

Types are not enforced as of this version.
"""

import typing

import pydantic
from pydantic import Field

from .types import BaseTypeId, ContinentId, ResourceId, ServerId


class BaseInfo(pydantic.BaseModel):
    """Static information for a given base.

    The contents of this payload only change with major game updates.
    API consumers can and should heavily cache the data returned to
    reduce API load (cache lifetime of hours to days).
    """

    id: int = Field(
        title='Base ID',
        description='Unique identifier of this base.',
        example=18204)
    continent_id: ContinentId = Field(
        title='Continent ID',
        description='The continent containing this base.',
        example=6)
    name: str = Field(
        title='Display Name',
        description='Display name of the base.',
        example='Cobalt Geological Outpost')
    map_pos: tuple[float, float] = Field(
        title='Map Position',
        description='A two-value tuple containing the X and Y coordinates at '
        'which the base marker should be placed on the map.',
        example=(-2602.2, -559.74))
    # Base type (BioLab, Small Outpost, etc.)
    type_id: BaseTypeId = Field(
        title='Type ID',
        description='Unique identifier of the facility type of the base.',
        example=9)
    type_name: str = Field(
        title='Type Name',
        description='Display name of the facility type of the base.',
        example='Construciton Outpost')
    # Outfit resources
    resource_amount: int = Field(
        title='Resource Amount',
        description='The amount of outfit resources awarded for capturing '
        'this base.',
        example=10)
    resource_id: typing.Optional[ResourceId] = Field(
        title='Resource ID',
        description='Unique identifier of the outfit resource type awarded '
        'for capturing this base.',
        example=2)
    resource_name: typing.Optional[str] = Field(
        title='Resource Name',
        description='Display name of the outfit resource type awarded for '
        'capturing this base.',
        example='Synthium')

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False


class ContinentInfo(pydantic.BaseModel):
    """Static information for a given continent.

    The contents of this payload only change with major game updates.
    API consumers can and should heavily cache the data returned to
    reduce API load (cache lifetime of hours to days).
    """

    id: ContinentId = Field(
        title='Continent ID',
        description='Unique identifier of this continent.',
        example=2)
    name: str = Field(
        title='Name',
        description='Display name of the continent.',
        example='Indar')
    # internal identifier used for map-specific assets
    code: str = Field(
        title='Asset Code',
        description='Internal identifier used for API-hosted art assets. '
        'See the API repository [README]'
        '(https://github.com/leonhard-s/ps2-map-api/blob/main/README.md) '
        'for details.',
        example='indar')
    description: str = Field(
        title='Description',
        description='A flavour text/description for the continent. Can be '
        'to fill in empty space on the map switcher.',
        example='The arid continent of Indar is home to multiple biomes, '
        'providing unique challenges for its combatants.')
    map_size: int = Field(
        title='Map Size',
        description='Base size of the map in in-game units. This is equal to '
        '8192 for most continents.',
        example=8192)
    lattice_links: list[tuple[int, int]] = Field(
        title='Lattice Links',
        description='A list of two-value integer tuples representing base '
        'connectivity. The integers represent the base IDs, the order of the '
        'base IDs is arbitrary.',
        example=[])

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False


class ServerInfo(pydantic.BaseModel):
    """Static information for a given server.

    The contents of this payload only change with major game updates.
    API consumers can and should heavily cache the data returned to
    reduce API load (cache lifetime of hours to days).
    """

    id: ServerId = Field(
        title='Server ID',
        description='Unique identifier of this server.',
        example=13)
    name: str = Field(
        title='Display Name',
        description='Display name of the server.',
        example='Cobalt')
    region: typing.Literal['Asia', 'EU', 'US West', 'US East'] = Field(
        title='Server Region',
        description='Geographical location of the server.',
        example='EU')

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False
