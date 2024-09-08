"""API routes for PS2 continents/zones."""

import fastapi

from ..database import Database, model_factory
from ..models import Continent
from ..sql import GET_CONTINENT_ALL_TRACKED

router = fastapi.APIRouter(prefix='/continent')


@router.get('', response_model=list[Continent])
async def continent() -> list[Continent]:
    """Static endpoint returning all available continents.

    This endpoint returns all continents (aka. zones) in the database,
    including ones for which no live map status is available (such as
    the tutorial zones or Sanctuary).

    This data only changes with very large game updates such as new
    continents being added to the game.

    API consumers are encouraged to cache this data locally, only
    updating their cache intermittently to stay up-to-date with game
    updates, e.g. once per day/week.
    """
    async with Database().pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(GET_CONTINENT_ALL_TRACKED)
            bases = await cur.fetchall()
    return [model_factory(Continent, b) for b in bases]
