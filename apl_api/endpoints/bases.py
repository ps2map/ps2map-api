"""API endpoints for map bases."""

import datetime
import random
from typing import List, Optional, cast

import fastapi

from ..interfaces import BaseInfo, BaseStatus
from ..types import BaseId, FactionData, FactionId, OutfitId, ServerId
from ._utils import IdListQuery, ids_from_string, static_from_json
from .outfits import _STATIC_OUTFIT_DATA as OUTFITS
from .servers import _STATIC_SERVER_DATA as SERVERS


router = fastapi.APIRouter(prefix='/bases')

_STATIC_BASE_DATA = static_from_json(BaseInfo, 'static_bases.json')


@router.get('/', response_model=List[BaseInfo])  # type: ignore
async def base_list() -> List[BaseInfo]:
    """Return a list of all static base data.

    Please note that this endpoint produces a large return object and
    may be retired in upcoming versions for performance reasons. Use
    the `bases/info` endpoint instead.
    """
    return list(_STATIC_BASE_DATA.values())


@router.get('/info', response_model=List[BaseInfo])  # type: ignore
async def base_info(base_id: str = IdListQuery,  # type: ignore
                    continent_id: str = IdListQuery,  # type: ignore
                    ) -> List[BaseInfo]:
    """Return static data for a given base.

    This includes properties like the base name or type. API consumers
    are expected to aggressively cache the returned data as they will
    only change with major game updates.

    Can be queried by either the `base_id` or `continent_id` field.
    """
    # Parse input
    base_ids = ids_from_string(base_id)
    continent_ids = ids_from_string(continent_id)
    # Validate input
    if not bool(base_ids) ^ bool(continent_ids):
        if base_ids:
            raise fastapi.HTTPException(
                400, 'Either base_id or continent_id must be specified')
        raise fastapi.HTTPException(
            400, 'base_id and continent_id are mutually exclusive')
    # Retrieve bases (only one of these for loops will run)
    data: List[BaseInfo] = []
    for id_ in base_ids:
        try:
            data.append(_STATIC_BASE_DATA[id_])
        except KeyError as err:
            msg = f'Unknown base ID: {id_}'
            raise fastapi.HTTPException(status_code=404, detail=msg) from err
    for id_ in continent_ids:
        for base in _STATIC_BASE_DATA.values():
            if base.continent_id == id_:
                data.append(base)
    return data


@router.get('/status', response_model=List[BaseStatus])  # type: ignore
async def base_status(base_id: str = IdListQuery,  # type: ignore
                      continent_id: str = IdListQuery,  # type: ignore
                      server_id: str = IdListQuery,  # type: ignore
                      ) -> List[BaseStatus]:
    """Return momentary status data for a base.

    Return the current status digest of a given base. This includes
    volatile data such as population or current ownership.

    This endpoint will likely be moved to or replicated in a WebSocket
    endpoint future versions.

    Can be queried by either the `base_id` or `continent_id` field. A
    valid `server_id` must always be provided.
    """
    # Parse input
    base_ids = ids_from_string(base_id)
    continent_ids = ids_from_string(continent_id)
    server_ids = ids_from_string(server_id)
    # Validate parameters
    if bool(base_ids) and bool(continent_ids):
        if base_ids:
            raise fastapi.HTTPException(
                400, 'Either base_id or continent_id must be specified')
        raise fastapi.HTTPException(
            400, 'base_id and continent_id are mutually exclusive')
    if not server_ids:
        raise fastapi.HTTPException(
            400, 'At least one server_id must be specified')
    for id_ in server_ids:
        if id_ not in SERVERS:
            msg = f'Unknown server ID: {id_}'
            raise fastapi.HTTPException(status_code=404, detail=msg)
    # Retrieve base data
    data: List[BaseStatus] = []
    for id_ in server_ids:
        # Make up random data
        for base_ in _STATIC_BASE_DATA:
            if base_ids and base_ not in base_ids:
                continue
            population: FactionData[int] = FactionData(
                vs=random.randint(0, 50),
                tr=random.randint(0, 50),
                nc=random.randint(0, 50),
                nso=random.randint(0, 5))
            faction = cast(FactionId, random.randint(1, 3))
            outfit: Optional[OutfitId] = None
            if random.random() < 0.75:
                outfit = random.choice(list(OUTFITS.values())).id
            data.append(
                BaseStatus(
                    id=cast(BaseId, base_),
                    server_id=cast(ServerId, id_),
                    population=population,
                    owning_faction=faction,
                    owning_outfit=outfit,
                    held_since=int(datetime.datetime.now().timestamp())))
    return data
