"""API routes for map bases."""

import datetime
import random
from typing import cast

import fastapi
from fastapi.params import Query
from pydantic.types import PositiveInt

from ..interfaces import BaseInfo, BaseStatus
from ..types import FactionId, OutfitId, Population, ServerId
from ._utils import static_from_json

# HACK: Load static development data
from .outfits import _STATIC_OUTFIT_DATA as OUTFITS  # type: ignore
from .servers import _STATIC_SERVER_DATA as SERVERS  # type: ignore


router = fastapi.APIRouter(prefix='/bases')

_STATIC_BASE_DATA = static_from_json(BaseInfo, 'static_bases.json')


@router.get('/info', response_model=list[BaseInfo])
async def base_info(
    continent_id: PositiveInt = Query(  # type: ignore
        ...,
        title='Continent ID',
        description='Unique identifier of the continent for which to return '
        'base information.'),
) -> list[BaseInfo]:
    """Return the list of bases for a given continent.

    This payload contains unchanging properties like the base name or
    type. API consumers are expected to aggressively cache the returned
    data as they will only change with major game updates.
    """
    data: list[BaseInfo] = []
    for base in _STATIC_BASE_DATA.values():
        if base.continent_id == continent_id:
            data.append(base)
    if not data:
        msg = f'No bases found for continent ID: {continent_id}'
        raise fastapi.HTTPException(status_code=404, detail=msg)
    return data


@router.get('/status', response_model=list[BaseStatus])
async def base_status(
    continent_id: PositiveInt = Query(  # type: ignore
        ...,
        title='Continent ID',
        description='Unique identifier of the continent for which to return '
        'a base status digest.'),
    server_id: PositiveInt = Query(  # type: ignore
        ...,
        title='Server ID',
        description='Unique identifier of the server for which to return a '
        'base status digest.')
) -> list[BaseStatus]:
    """Return a momentary status digest for all bases on a continent.

    This endpoint will likely be moved to or replicated in a WebSocket
    endpoint in future versions.
    """
    if server_id not in SERVERS:
        msg = f'Unknown server ID: {server_id}'
        raise fastapi.HTTPException(status_code=404, detail=msg)
    data: list[BaseStatus] = []
    # Make up random data
    for base in _STATIC_BASE_DATA.values():
        if base.continent_id != continent_id:
            continue
        population = Population(
            vs=random.randint(0, 50),
            tr=random.randint(0, 50),
            nc=random.randint(0, 50),
            nso=random.randint(0, 5))
        faction = cast(FactionId, random.randint(1, 3))
        outfit: OutfitId | None = None
        if random.random() < 0.75:
            outfit = random.choice(list(OUTFITS.values())).id
        data.append(
            BaseStatus(
                id=base.id,
                server_id=cast(ServerId, server_id),
                population=population,
                owning_faction=faction,
                owning_outfit=outfit,
                held_since=int(datetime.datetime.now().timestamp())))
    if not data:
        msg = f'No bases found for continent ID: {continent_id}'
        raise fastapi.HTTPException(status_code=404, detail=msg)
    return data
