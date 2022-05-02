"""API routes for PS2 game servers."""

import random
from typing import cast

import fastapi

from ..interfaces import ServerInfo, ServerStatus
from ..types import ContinentId, Population
from ._utils import static_from_json


router = fastapi.APIRouter(prefix='/servers')

_STATIC_SERVER_DATA = static_from_json(ServerInfo, 'static_servers.json')


@router.get('/info', response_model=list[ServerInfo])
async def server_info() -> list[ServerInfo]:
    """Return the list of servers.

    This payload contains unchanging properties like the server name or
    region. API consumers are expected to aggressively cache the
    returned data as they will only change with major game updates.
    """
    return list(_STATIC_SERVER_DATA.values())


@router.get('/status', response_model=list[ServerStatus])
async def server_status() -> list[ServerStatus]:
    """Return a momentary status digest for all servers.

    This endpoint will likely be moved to or replicated in a WebSocket
    endpoint in future versions.
    """
    data: list[ServerStatus] = []
    for server in _STATIC_SERVER_DATA.values():
        # Make up random data
        status = 'online' if random.random() < 0.9 else 'locked'
        base_pop = random.randint(10, 300)
        population = Population(
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
                id=server.id,
                status=status,
                population=population,
                open_continents=continents))
    return data
