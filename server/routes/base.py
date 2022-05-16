"""API routes for map bases."""

import fastapi
from fastapi.params import Query

from ..database import Database, model_factory
from ..models import Base

router = fastapi.APIRouter(prefix='/base')


@router.get('', response_model=list[Base])
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
    async with Database().pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute('SELECT * FROM "API_static"."BaseInfo" '
                              'WHERE "continent_id" = %s;', (continent_id,))
            bases = await cur.fetchall()
    if not bases:
        msg = f'No bases found for continent ID: {continent_id}'
        raise fastapi.HTTPException(status_code=404, detail=msg)
    return [model_factory(Base, b) for b in bases]
