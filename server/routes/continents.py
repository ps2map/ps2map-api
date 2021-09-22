"""API routes for PS2 continents/zones."""

import datetime
import random
from typing import List, cast

import fastapi
from fastapi.params import Query
from pydantic.types import PositiveInt

from ..interfaces import ContinentInfo, ContinentStatus
from ..types import FactionId, Population, ServerId
from ._utils import static_from_json
from .servers import _STATIC_SERVER_DATA as SERVERS

router = fastapi.APIRouter(prefix='/continents')

_STATIC_CONTINENT_DATA = static_from_json(
    ContinentInfo, 'static_continents.json')


@router.get('/info', response_model=List[ContinentInfo])  # type: ignore
async def continent_info() -> List[ContinentInfo]:
    """Return static continent data.

    This includes properties like the continent name or description.
    API consumers are expected to aggressively cache the returned data
    as they will only change with major game updates.
    """
    return list(_STATIC_CONTINENT_DATA.values())


@router.get('/status', response_model=List[ContinentStatus])  # type: ignore
async def continent_status(
    server_id: PositiveInt = Query(  # type: ignore
        ...,
        title='Server ID',
        description='Unique identifier of the server for which to return a '
        'continent status digest.'
    )
) -> List[ContinentStatus]:
    """Return a momentary status digest for all continents.

    This endpoint will likely be moved to or replicated in a WebSocket
    endpoint in future versions.
    """
    if server_id not in SERVERS:
        msg = f'Unknown server ID: {server_id}'
        raise fastapi.HTTPException(status_code=404, detail=msg)
    data: List[ContinentStatus] = []
    for continent in _STATIC_CONTINENT_DATA.values():
        status = 'locked' if random.random() < 0.6 else 'open'
        locked = bool(status == 'locked')
        if locked:
            population = Population(
                vs=0, nc=0, tr=0, nso=0)
            locked_by = cast(FactionId, random.randint(1, 3))
            alert_active = False
            alert_started = None
            alert_ends = None
        else:
            population = Population(
                vs=random.randint(50, 300),
                nc=random.randint(50, 300),
                tr=random.randint(50, 300),
                nso=random.randint(0, 10))
            locked_by = None
            alert_active = random.random() < 0.5
            alert_started = None
            alert_ends = None
            if alert_active:
                start = (
                    datetime.datetime.now()
                    - datetime.timedelta(minutes=random.randint(5, 80)))
                alert_started = int(start.timestamp())
                alert_ends = int(
                    (start + datetime.timedelta(minutes=90)).timestamp())
            print(continent)
        data.append(
            ContinentStatus(
                id=continent.id,
                server_id=cast(ServerId, server_id),
                population=population,
                status=status,
                locked_by=locked_by,
                alert_active=alert_active,
                alert_started=alert_started,
                alert_ends=alert_ends))
    return data
