"""Dataclass representations of payloads sent between the DB and API.

Types are not enforced as of this version.
"""

import datetime
import typing

import pydantic
from pydantic import Field

from .types import (BaseId, BaseTypeId, ContinentId, FactionId, Population,
                    OutfitId, OutfitTag, ResourceId, ServerId)

# Used for example timestamps
_startup_time = int(datetime.datetime.now().timestamp())


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


class BaseStatus(pydantic.BaseModel):
    """A dynamic update message for a given base.

    The contents of this payload are dynamic and will change regularly.

    This payload will likely be replicated in or moved to a WebSocket
    endpoint in an upcoming API version.
    """

    id: BaseId = Field(
        title='Base ID',
        description='Unique identifier of the base being updated.',
        example=18025)
    server_id: ServerId = Field(
        title='Server ID',
        description='Unique identifier of the server for which the base '
        'should be updated.',
        example=13)
    population: Population = Field(
        title='Population',
        description='A mapping of faction identifiers to the current '
        'population estimate.',
        example={'vs': 37, 'nc': 28, 'tr': 13, 'nso': 5})
    owning_faction: typing.Optional[FactionId] = Field(
        title='Owning Faction',
        description='Unique identifier of the faction currently in control of '
        'the facility. Locked or otherwise inaccessible facilities will '
        'return NULL rather than 0.',
        example=2)
    owning_outfit: typing.Optional[OutfitId] = Field(example=None)
    held_since: int = Field(example=_startup_time)

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


class ContinentStatus(pydantic.BaseModel):
    """A dynamic update message for a given continent.

    The contents of this payload are dynamic and will change regularly.

    This payload will likely be replicated in or moved to a WebSocket
    endpoint in an upcoming API version.
    """

    id: ContinentId = Field(
        title='Continent ID',
        description='Unique identifier of the continent being updated.',
        example=4)
    server_id: ServerId = Field(
        title='Server ID',
        description='Unique identifier of the server for which the continent '
        'should be updated.',
        example=10)
    population: Population = Field(
        title='Population',
        description='A mapping of faction identifiers to the current '
        'population estimate.',
        example={'vs': 123, 'nc': 112, 'tr': 126, 'nso': 8})
    status: typing.Literal['open', 'locked'] = Field(
        title='Status',
        description='A string value representing the current status of the '
        'continent. More values may be added, use comparisons to the string '
        '`"locked"` to determine whether the continent is open.',
        example='open')
    locked_by: typing.Optional[int] = Field(
        title='Locked By',
        description='For continents whose `status` is `"locked"`, this field '
        'specifies which empire locked the continent. NULL for open '
        'continents.',
        example=None)
    # Alert status
    alert_active: bool = Field(
        title='Alert Active Flag',
        description='Whether there is an ongoing alert on the continent.',
        example=True)
    alert_started: typing.Optional[int] = Field(
        title='Alert Start Timestamp',
        description='UTC timestamp of when the ongoing alert started. NULL '
        'whenever the `alert_active` flag is false.',
        example=_startup_time)
    alert_ends: typing.Optional[int] = Field(
        title='Alert End Timestamp',
        description='UTC timestamp of when the ongoing alert is scheduled to '
        'end. NULL whenever the `alert_active` flag is false.',
        example=_startup_time + 5400)

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


class ServerStatus(pydantic.BaseModel):
    """A dynamic update message for a given base.

    The contents of this payload are dynamic and will change regularly.

    This payload will likely be replicated in or moved to a WebSocket
    endpoint in an upcoming API version.
    """

    id: ServerId = Field(
        title='Server ID',
        description='Unique identifier of the server being updated',
        example=40)
    status: typing.Literal['online', 'locked'] = Field(
        title='Server Status',
        description='Current status of the server. The literals listed as the '
        'type are tentative and may change in future versions.',
        example='online')
    population: Population = Field(
        title='Population',
        description='A mapping of faction identifiers to the current '
        'population estimate.',
        example={'vs': 251, 'nc': 221, 'tr': 246, 'nso': 16})
    open_continents: list[ContinentId] = Field(example=[2, 6])

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False


class OutfitInfo(pydantic.BaseModel):
    """Static information for a given outfit.

    The contents of this payload may change from one day to the next.
    API consumers are still recommended to cache the data returned, but
    cache lifetime should only be a few hours as outfit tags can change
    at any time.
    """

    id: OutfitId = Field(
        title='Outfit ID',
        description='Unique identifier of this outfit.',
        example=37564049462661850)
    faction_id: FactionId = Field(
        title='Faction ID',
        description='Unique identifier of the faction this outfit is on.',
        example=1)
    server_id: ServerId = Field(
        title='Server ID',
        description='Unique identifier of the server on which this outfit '
        'lives.',
        example=13)
    name: str = Field(
        title='Outfit Name',
        description='The custom name of this outfit.',
        example='Urge to Confess')
    tag: typing.Optional[OutfitTag] = Field(
        title='Outfit Tag',
        description='The unique tag of the outfit.',
        example='URGE')

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False
