"""Dataclass representations of payloads sent between the DB and API.

Types are not enforced as of this version.
"""

import datetime
import dataclasses
from typing import List, Optional, Tuple

from .types import FactionData, OutfitInfo


@dataclasses.dataclass(frozen=True)
class ServerInfo:
    """Response object for server info queries."""

    server_id: int
    name: str
    status: str
    region: str
    population: FactionData[float]


@dataclasses.dataclass(frozen=True)
class ContinentInfo:
    """Reponse object for continent info queries."""

    continent_id: int
    name: str
    status: str


@dataclasses.dataclass(frozen=True)
class LatticeInfo:
    continent_id: int
    links: List[Tuple[int, int]]


@dataclasses.dataclass(frozen=True)
class ContinentUpdate:
    """Detailed information on a given continent's lattice."""

    continent_id: int
    locked_by: Optional[int]
    population: FactionData[float]


@dataclasses.dataclass(frozen=True)
class BaseInfo:
    """Base data that generally does not change."""

    base_id: int
    name: str
    continent_id: int
    map_position: Tuple[float, float]
    outline: str  # SVG outline


@dataclasses.dataclass(frozen=True)
class BaseUpdate:
    """Intermittent info for a given base."""

    base_id: int
    held_since: datetime.datetime
    faction: int
    outfit: Optional[OutfitInfo]
