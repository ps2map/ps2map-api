"""API routes for map bases."""

import fastapi
from fastapi.params import Query

from ..interfaces import BaseInfo
from ..types import BaseId

router = fastapi.APIRouter(prefix='/bases')


@router.get('/info', response_model=list[BaseInfo])
async def base_info(
    continent_id: BaseId = Query(  # type: ignore
        ...,
        title='Continent ID',
        description='Unique identifier of the continent for which to return '
        'base information.'),
) -> list[BaseInfo]:
    """Return the list of bases for a given continent.

    This payload contains unchanging properties like the base name or
    type. API consumers are expected to aggressively cache the returned
    data as they will only change with major game updates.
    """
    data: list[BaseInfo] = []
    if not data:
        msg = f'No bases found for continent ID: {continent_id}'
        raise fastapi.HTTPException(status_code=404, detail=msg)
    return data
