"""API endpoints for PS2 game servers."""

import asyncpg
import fastapi
from starlette.responses import JSONResponse

from .. import _db as database

router = fastapi.APIRouter(prefix='/servers')

_dep_pool = fastapi.Depends(database.get_pool)  # type: ignore


@router.get('/')  # type: ignore
async def get_servers(pool: asyncpg.pool.Pool = _dep_pool) -> JSONResponse:
    server_list = await database.get_servers(pool)
    return JSONResponse({'server_list': server_list})
