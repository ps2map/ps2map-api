"""API routes for PS2 continents/zones."""

import fastapi

from ..database import Database, model_factory
from ..models import Continent

router = fastapi.APIRouter(prefix='/continent')


@router.get('', response_model=list[Continent])
async def continent() -> list[Continent]:
    """Return static continent data.

    This includes properties like the continent name or description.
    API consumers are expected to aggressively cache the returned data
    as they will only change with major game updates.
    """
    async with Database().pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute('SELECT * FROM "API_static"."Continent";')
            bases = await cur.fetchall()
    return [model_factory(Continent, b) for b in bases]
