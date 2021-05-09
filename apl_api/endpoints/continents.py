"""API endpoints for PS2 continents/zones."""

import datetime
import random
from typing import List, cast

import fastapi

from ..interfaces import ContinentInfo, ContinentStatus
from ..types import ContinentId, FactionId, Population, ServerId
from ._utils import IdListQuery, ids_from_string, static_from_json
from .servers import _STATIC_SERVER_DATA as SERVERS

router = fastapi.APIRouter(prefix='/continents')

_STATIC_CONTINENT_DATA = static_from_json(
    ContinentInfo, 'static_continents.json')


@router.get('/', response_model=List[ContinentInfo])  # type: ignore
async def continent_list() -> List[ContinentInfo]:
    """Return a list of all static continent data.

    Please note that this endpoint produces a large return object and
    may be retired in upcoming versions for performance reasons. Use
    the `continents/info` endpoint instead.
    """
    return list(_STATIC_CONTINENT_DATA.values())


@router.get('/info', response_model=List[ContinentInfo])  # type: ignore
async def continent_info(continent_id: str = IdListQuery  # type: ignore
                         ) -> List[ContinentInfo]:
    """Return static data for a given continent.

    This includes properties like the continent name or description.
    API consumers are expected to aggressively cache the returned data
    as they will only change with major game updates.
    """
    # Parse input
    continent_ids = ids_from_string(continent_id)
    # Validate input
    if not continent_ids:
        raise fastapi.HTTPException(
            400, 'At least one continent_id must be specified')
    # Retrieve server data
    data: List[ContinentInfo] = []
    for id_ in continent_ids:
        try:
            data.append(_STATIC_CONTINENT_DATA[id_])
        except KeyError as err:
            msg = f'Unknown continent ID: {id_}'
            raise fastapi.HTTPException(status_code=404, detail=msg) from err
    return data


@router.get('/status', response_model=List[ContinentStatus])  # type: ignore
async def continent_status(continent_id: str = IdListQuery,  # type: ignore
                           server_id: str = IdListQuery  # type: ignore
                           ) -> List[ContinentStatus]:
    """Return momentary status data for a continent.

    Return the current status digest of a given continent. This
    includes volatile data such as population or ongoing alerts.

    This endpoint will likely be moved to or replicated in a WebSocket
    endpoint in future versions.
    """
    # Parse input
    continent_ids = ids_from_string(continent_id)
    server_ids = ids_from_string(server_id)
    # Validate parameters
    if not continent_id:
        raise fastapi.HTTPException(
            400, 'At least one continent_id must be specified')
    if not server_ids:
        raise fastapi.HTTPException(
            400, 'At least one server_id must be specified')
    for id_ in server_ids:
        if id_ not in SERVERS:
            msg = f'Unknown server ID: {id_}'
            raise fastapi.HTTPException(status_code=404, detail=msg)
    # Retrieve base data
    data: List[ContinentStatus] = []
    for id_ in server_ids:
        # Make up random data
        for cont in continent_ids:
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
            data.append(
                ContinentStatus(
                    id=cast(ContinentId, cont),
                    server_id=cast(ServerId, id_),
                    population=population,
                    status=status,
                    locked_by=locked_by,
                    alert_active=alert_active,
                    alert_started=alert_started,
                    alert_ends=alert_ends))
    return data
