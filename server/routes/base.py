"""API routes for map bases."""

import fastapi
from fastapi.params import Query

from ..database import Database, model_factory
from ..models import Base, BaseStatus
from ..sql import GET_BASE_BY_CONTINENT, GET_BASE_STATUS

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
            await cur.execute(GET_BASE_BY_CONTINENT, (continent_id,))
            bases = await cur.fetchall()
    return [model_factory(Base, b) for b in bases]


@router.get('/status', response_model=list[BaseStatus])
async def base_status(
    continent_id: int = Query(  # type: ignore
        ...,
        title='Continent ID',
        description='Unique ID of the continent for which to return base '
        'status information.'),
    server_id: int = Query(  # type: ignore
        ...,
        title='Server ID',
        description='Game server ID for which to return base status '
        'information.'),
) -> list[BaseStatus]:
    """Dynamic endpoint returning base status information.

    This endpoint is updated close to real time as bases are captured.
    """
    async with Database().pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(GET_BASE_STATUS, (continent_id, server_id))
            bases = await cur.fetchall()
    return [model_factory(BaseStatus, b) for b in bases]
