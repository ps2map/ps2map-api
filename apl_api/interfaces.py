"""Dataclass representations of payloads sent between the DB and API.

Types are not enforced as of this version.
"""

import dataclasses
from typing import List, Literal, Optional, Tuple

from .types import (BaseId, BaseTypeId, ContinentId, FactionId, FactionData,
                    OutfitId, OutfitTag, ResourceId, ServerId)


@dataclasses.dataclass(frozen=True)
class _Static:
    """Base class for static map data.

    This includes base or continent names, map hex outlines and other
    information that only changes with game upates (i.e. in-between app
    launches).
    """


@dataclasses.dataclass(frozen=True)
class _Dynamic:
    """Base class for dynamic map data.

    This includes current population, facility ownership and the
    continents available for each server. Data of this type can either
    be polled or received via a WebSocket interface whenever it
    changes.
    """


@dataclasses.dataclass(frozen=True)
class BaseInfo(_Static):
    """Static, unchanging base data."""

    id: BaseId
    continent_id: ContinentId
    name: str
    map_pos: Tuple[float, float]
    # Base type (BioLab, Small Outpost, etc.)
    type_id: BaseTypeId
    type_name: str
    # Outfit resources
    # NOTE: Rewards are not consistent within a base type.
    resource_amount: int
    resource_id: Optional[ResourceId]
    resource_name: Optional[str]


@dataclasses.dataclass(frozen=True)
class BaseStatus(_Dynamic):
    """Dynamic base state update."""

    id: BaseId
    server_id: ServerId
    population: FactionData[int]
    owning_faction: Optional[FactionId]
    owning_outfit: Optional[OutfitId]
    held_since: int


@dataclasses.dataclass(frozen=True)
class ContinentInfo(_Static):
    """Static, unchanging continent data."""

    id: ContinentId
    name: str
    description: str
    lattice_links: List[Tuple[int, int]]
    map_tileset: str  # Unique tileset identifier for the frontend


@dataclasses.dataclass(frozen=True)
class ContinentStatus(_Dynamic):
    """Dynamic continent state update."""

    id: ContinentId
    server_id: ServerId
    population: FactionData[int]
    status: Literal['open', 'locked']
    locked_by: Optional[int]
    # Alert status
    alert_active: bool
    alert_started: Optional[int]
    alert_ends: Optional[int]


@dataclasses.dataclass(frozen=True)
class ServerInfo(_Static):
    """Static, unchanging server data."""

    id: ServerId
    name: str
    region: Literal['Asia', 'EU', 'US West', 'US East']


@dataclasses.dataclass(frozen=True)
class ServerStatus(_Dynamic):
    """Dynamic server state update."""

    id: ServerId
    status: Literal['online', 'locked']
    population: FactionData[int]
    open_continents: List[ContinentId]


@dataclasses.dataclass(frozen=True)
class OutfitInfo(_Static):
    """Static, unchanging outfit data."""

    id: OutfitId
    faction_id: FactionId
    server_id: ServerId
    name: str
    tag: Optional[OutfitTag]
