"""API routes for map bases."""

import fastapi
from fastapi.params import Query

from ..database import Database, model_factory
from ..models import Base, BaseStatus
from ..sql import GET_BASE_BY_CONTINENT, GET_BASE_STATUS

router = fastapi.APIRouter(prefix='/base')


def _code_from_base_id(type_id: int) -> str:
    if type_id == 2:
        return 'amp-station'
    if type_id == 3:
        return 'bio-lab'
    if type_id == 4:
        return 'tech-plant'
    if type_id == 5:
        return 'large-outpost'
    if type_id == 6:
        return 'small-outpost'
    if type_id == 7:
        return 'warpgate'
    if type_id == 8:
        return 'interlink'
    if type_id == 9:
        return 'construction-outpost'
    if type_id == 11:
        return 'containment-site'
    if type_id == 12:
        return 'trident'
    if type_id == 13:
        # seapost
        return 'small-outpost'
    if type_id == 14:
        # large CTF outpost
        return 'large-outpost'
    if type_id == 15:
        # small CTF outpost
        return 'small-outpost'
    if type_id == 16:
        # Amp Station CTF
        return 'amp-station'
    return 'unknown'


def _code_from_resource_id(resource_id: int) -> str:
    if resource_id == 1:
        return 'auraxium'
    if resource_id == 2:
        return 'synthium'
    if resource_id == 3:
        return 'polystellarite'
    return 'unknown'


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
    models: list[Base] = []
    for base in bases:
        base_patched = Base(
            id=base[0],
            continent_id=base[1],
            name=base[2],
            map_pos=[base[3], base[4]],
            type_name=base[5],
            type_code=_code_from_base_id(base[6]),
            resource_capture_amount=base[7],
            resource_control_amount=base[8],
            resource_name=base[9],
            resource_code=_code_from_resource_id(base[10]),
        )
        models.append(base_patched)
    return models


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
