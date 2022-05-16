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
    """Static endpoint returning bases on a per-continent basis.

    This data only changes with major game updates such as continent
    reworks, lattice tweaks, or outfit resource reward adjustments.

    API consumers are encouraged to cache this data locally, only
    updating their cache intermittently to stay up-to-date with game
    updates, e.g. once per day/week.
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
