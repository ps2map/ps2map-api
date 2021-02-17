"""API endpoints for PS2 game servers."""

import dataclasses

import fastapi
from starlette.responses import JSONResponse

from ..interfaces import ServerInfo
from ..types import FactionData

router = fastapi.APIRouter(prefix='/servers')


@router.get('/')  # type: ignore
async def get_servers() -> JSONResponse:
    servers = [
        ServerInfo(1, 'Connery', 'high', 'US West',
                   FactionData(28.0, 33.0, 34.0, 5.0)),
        ServerInfo(10, 'Miller', 'high', 'EU',
                   FactionData(33.0, 34.0, 32.0, 1.0)),
        ServerInfo(13, 'Cobalt', 'medium', 'EU',
                   FactionData(34.0, 33.0, 33.0, 0.0)),
        ServerInfo(17, 'Emerald', 'medium', 'US East',
                   FactionData(39.0, 35.0, 30.0, 2.0)),
        ServerInfo(40, 'SolTech', 'low', 'Asia',
                   FactionData(32.0, 34.0, 31.0, 3.0))
    ]
    server_list = [dataclasses.asdict(d) for d in servers]
    return JSONResponse({'server_list': server_list})
