"""API endpoints for PS2 player outfits."""

from typing import List, cast

import fastapi
from fastapi.params import Query

from ..interfaces import OutfitInfo
from ..types import OutfitId
from ._utils import static_from_json

router = fastapi.APIRouter(prefix='/outfits')

_STATIC_OUTFIT_DATA = static_from_json(OutfitInfo, 'static_outfits.json')


@router.get('/info', response_model=List[OutfitInfo])  # type: ignore
async def outfit_info(
    outfit_id: List[int] = Query(  # type: ignore
        ...,
        title='Outfit ID',
        description='Unique identifier of the outfit to return. May be '
        'specified multiple times to retrieve data for multiple outfits.')
) -> List[OutfitInfo]:
    """Return static data for the given outfit.

    This includes basic fields for display on the map, like the outfit
    name, faction, or tag. API consumers are expected to cache the
    returned data.
    """
    # Retrieve server data
    data: List[OutfitInfo] = []
    for id_ in outfit_id:
        try:
            data.append(_STATIC_OUTFIT_DATA[cast(OutfitId, id_)])
        except KeyError as err:
            msg = f'Unknown outfit ID: {id_}'
            raise fastapi.HTTPException(status_code=404, detail=msg) from err
    return data
