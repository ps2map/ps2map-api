"""API endpoints for PS2 continents/zones."""

import dataclasses

import fastapi
from starlette.responses import JSONResponse

from ..interfaces import ContinentInfo

router = fastapi.APIRouter(prefix='/continents')


@router.get('/')  # type: ignore
async def get_continents() -> JSONResponse:
    continents = [
        ContinentInfo(2, 'Indar', 'open'),
        ContinentInfo(4, 'Hossin', 'locked'),
        ContinentInfo(6, 'Amerish', 'open'),
        ContinentInfo(8, 'Esamir', 'locked')
    ]
    continent_list = [dataclasses.asdict(d) for d in continents]
    return JSONResponse({'continent_list': continent_list})
