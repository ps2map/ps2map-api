"""API endpoints for PS2 continents/zones."""

import asyncpg
import fastapi
from starlette.responses import JSONResponse

from .. import _db as database

router = fastapi.APIRouter(prefix='/continents')

_dep_pool = fastapi.Depends(database.get_pool)  # type: ignore


@router.get('/')  # type: ignore
async def get_continents(pool: asyncpg.pool.Pool = _dep_pool) -> JSONResponse:
    continent_list = await database.get_continents(pool)
    return JSONResponse({'continent_list': continent_list})
