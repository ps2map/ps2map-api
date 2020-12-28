"""API endpoints for PS2 continents/zones."""

import fastapi
from starlette.responses import JSONResponse

from .. import _db as database

router = fastapi.APIRouter(prefix='/continents')


@router.get('/')  # type: ignore
async def get_continents() -> JSONResponse:
    continent_list = await database.get_continents()
    return JSONResponse({'continent_list': continent_list})
