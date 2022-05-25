"""API routes for lattice links between two bases."""

import fastapi
from fastapi.params import Query

from ..database import Database, model_factory
from ..models import LatticeLink
from ..sql import GET_LATTICE_BY_CONTINENT

router = fastapi.APIRouter(prefix='/lattice')


@router.get('', response_model=list[LatticeLink])
async def lattice(
    continent_id: int = Query(  # type: ignore
        ...,
        title='Continent ID',
        description='Unique ID of the continent for which to return the list '
        'of lattice links.'),
) -> list[LatticeLink]:
    """Static endpoint returning lattice links for a given continent.

    This endpoint returns pairs of bases that are connected by the game
    lattice, i.e. that can be attacked from one base to the other.

    The returned payload contains both the IDs of the bases, and the
    X and Y coordinates of their respective map positions.

    This data only changes with major game updates such as major
    continent reworks.

    API consumers are encouraged to cache this data locally, only
    updating their cache intermittently to stay up-to-date with game
    updates, e.g. once per day/week.
    """
    async with Database().pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(GET_LATTICE_BY_CONTINENT, (continent_id,))
            links = await cur.fetchall()
    return [model_factory(LatticeLink, l) for l in links]
