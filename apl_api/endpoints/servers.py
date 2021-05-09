"""API endpoints for PS2 game servers."""

import random
from typing import List, cast

import fastapi

from ..interfaces import ServerInfo, ServerStatus
from ..types import ContinentId, FactionData, ServerId
from ._utils import IdListQuery, ids_from_string, static_from_json


router = fastapi.APIRouter(prefix='/servers')

_STATIC_SERVER_DATA = static_from_json(ServerInfo, 'static_servers.json')


@router.get('/', response_model=List[ServerInfo])  # type: ignore
async def server_list() -> List[ServerInfo]:
    return list(_STATIC_SERVER_DATA.values())


@router.get('/info', response_model=List[ServerInfo])  # type: ignore
async def server_info(server_id: str = IdListQuery  # type: ignore
                      ) -> List[ServerInfo]:
    # Parse input
    server_ids = ids_from_string(server_id)
    # Validate input
    if not server_ids:
        raise fastapi.HTTPException(
            400, 'At least one server_id must be specified')
    # Retrieve server data
    data: List[ServerInfo] = []
    for id_ in server_ids:
        try:
            data.append(_STATIC_SERVER_DATA[id_])
        except KeyError as err:
            msg = f'Unknown server ID: {id_}'
            raise fastapi.HTTPException(status_code=404, detail=msg) from err
    return data


@router.get('/status', response_model=List[ServerStatus])  # type: ignore
async def server_status(server_id: str = IdListQuery  # type: ignore
                        ) -> List[ServerStatus]:
    # Parse input
    server_ids = ids_from_string(server_id)
    # Validate input
    if not server_ids:
        raise fastapi.HTTPException(
            400, 'At least one server_id must be specified')
    # Retrieve server data
    data: List[ServerStatus] = []
    for id_ in server_ids:
        if id_ not in _STATIC_SERVER_DATA:
            msg = f'Unknown server ID: {id_}'
            raise fastapi.HTTPException(status_code=404, detail=msg)
        # Make up random data
        status = 'online' if random.random() < 0.9 else 'locked'
        base_pop = random.randint(10, 300)
        population: FactionData[int] = FactionData(
            vs=base_pop + random.randint(0, 100),
            nc=base_pop + random.randint(0, 100),
            tr=base_pop + random.randint(0, 100),
            nso=int(base_pop*0.05))
        continents = [cast(ContinentId, i)
                      for i in (2, 4, 6, 8) if random.random() < 0.5]
        if not continents:
            continents.append(cast(ContinentId, 2))
        data.append(
            ServerStatus(
                id=cast(ServerId, id_),
                status=status,
                population=population,
                open_continents=continents))
    return data
