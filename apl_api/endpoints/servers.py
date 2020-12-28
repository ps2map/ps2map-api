"""API endpoints for PS2 game servers."""

import fastapi
from starlette.responses import JSONResponse

from .. import _db as database

router = fastapi.APIRouter(prefix='/servers')


@router.get('/')  # type: ignore
async def get_servers() -> JSONResponse:
    server_list = await database.get_servers()
    return JSONResponse({'server_list': server_list})
