"""API routes for map bases."""

import fastapi
from fastapi.params import Query

from ..models import Base

router = fastapi.APIRouter(prefix='/base')


@router.get('/', response_model=list[Base])
async def base(
    continent_id: int = Query(  # type: ignore
        ...,
        title='Continent ID',
        description='Unique ID of the continent for which to return base '
        'information.'),
) -> list[Base]:
    """Return the list of bases for a given continent.

    This payload contains unchanging properties like the base name or
    type. API consumers are expected to aggressively cache the returned
    data as they will only change with major game updates.
    """
    data: list[Base] = []
    if not data:
        msg = f'No bases found for continent ID: {continent_id}'
        raise fastapi.HTTPException(status_code=404, detail=msg)
    return data
