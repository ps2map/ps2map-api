"""API endpoints for PS2 player outfits."""

import dataclasses
from typing import List

import fastapi
from starlette.responses import JSONResponse

from ..interfaces import OutfitInfo
from ._utils import IdListQuery, ids_from_string, static_from_json

router = fastapi.APIRouter(prefix='/outfits')

_STATIC_OUTFIT_DATA = static_from_json(OutfitInfo, 'static_outfits.json')


@router.get('/')  # type: ignore
async def root() -> JSONResponse:
    """Return a list of all cached outfit data.

    Please note that this endpoint produces a large return object and
    may be retired in upcoming versions for performance reasons. Use
    the `outfits/info` endpoint instead.
    """
    return JSONResponse(
        [dataclasses.asdict(d) for d in _STATIC_OUTFIT_DATA.values()])


@router.get('/info')  # type: ignore
async def outfit_info(outfit_id: str = IdListQuery  # type: ignore
                      ) -> JSONResponse:
    """Return static data for a given outfit.

    This includes basic fields for display on the map, like the outfit
    name, faction, or tag. API consumers are expected to cache the
    returned data.
    """
    # Parse input
    outfit_ids = ids_from_string(outfit_id)
    # Validate input
    if not outfit_ids:
        raise fastapi.HTTPException(
            400, 'At least one outfit_id must be specified')
    # Retrieve server data
    data: List[OutfitInfo] = []
    for id_ in outfit_ids:
        try:
            data.append(_STATIC_OUTFIT_DATA[id_])
        except KeyError as err:
            msg = f'Unknown outfit ID: {id_}'
            raise fastapi.HTTPException(status_code=404, detail=msg) from err
    return JSONResponse([dataclasses.asdict(d) for d in data])
