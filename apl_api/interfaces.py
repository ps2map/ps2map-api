"""Dataclass representations of payloads sent between the DB and API.

Types are not enforced as of this version.
"""

from typing import List, Literal, Optional, Tuple

import pydantic

from .types import (BaseId, BaseTypeId, ContinentId, FactionId, FactionData,
                    OutfitId, OutfitTag, ResourceId, ServerId)


class BaseInfo(pydantic.BaseModel):
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

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False


class BaseStatus(pydantic.BaseModel):
    """Dynamic base state update."""

    id: BaseId
    server_id: ServerId
    population: FactionData[int]
    owning_faction: Optional[FactionId]
    owning_outfit: Optional[OutfitId]
    held_since: int

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False


class ContinentInfo(pydantic.BaseModel):
    """Static, unchanging continent data."""

    id: ContinentId
    name: str
    code: str  # internal identifier used for map-specific assets
    description: str
    lattice_links: List[Tuple[int, int]]

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False


class ContinentStatus(pydantic.BaseModel):
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

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False


class ServerInfo(pydantic.BaseModel):
    """Static, unchanging server data."""

    id: ServerId
    name: str
    region: Literal['Asia', 'EU', 'US West', 'US East']

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False


class ServerStatus(pydantic.BaseModel):
    """Dynamic server state update."""

    id: ServerId
    status: Literal['online', 'locked']
    population: FactionData[int]
    open_continents: List[ContinentId]

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False


class OutfitInfo(pydantic.BaseModel):
    """Static, unchanging outfit data."""

    id: OutfitId
    faction_id: FactionId
    server_id: ServerId
    name: str
    tag: Optional[OutfitTag]

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False
