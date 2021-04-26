"""API endpoints for PS2 continents/zones."""

import dataclasses
import datetime
import random
from typing import List, cast

import fastapi
from starlette.responses import JSONResponse

from ..interfaces import ContinentInfo, ContinentStatus
from ..types import ContinentId, FactionData, FactionId, ServerId
from ._utils import IdListQuery, ids_from_string, static_from_json
from .servers import _STATIC_SERVER_DATA as SERVERS

router = fastapi.APIRouter(prefix='/continents')

_STATIC_CONTINENT_DATA = static_from_json(
    ContinentInfo, 'static_continents.json')


@router.get('/')  # type: ignore
async def root() -> JSONResponse:
    return JSONResponse(
        [dataclasses.asdict(d) for d in _STATIC_CONTINENT_DATA.values()])


@router.get('/info')  # type: ignore
async def continent_info(continent_id: str = IdListQuery  # type: ignore
                         ) -> JSONResponse:
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
    return JSONResponse([dataclasses.asdict(d) for d in data])


@router.get('/status')  # type: ignore
async def continent_status(continent_id: str = IdListQuery,  # type: ignore
                           server_id: str = IdListQuery  # type: ignore
                           ) -> JSONResponse:
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
                population = FactionData(0, 0, 0, 0)
                locked_by = cast(FactionId, random.randint(1, 3))
                alert_active = False
                alert_started = None
                alert_ends = None
            else:
                population = FactionData(
                    random.randint(50, 300),
                    random.randint(50, 300),
                    random.randint(50, 300),
                    random.randint(0, 10))
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
                    cast(ContinentId, cont), cast(ServerId, id_),
                    population, status, locked_by,
                    alert_active,
                    alert_started,
                    alert_ends))
    return JSONResponse([dataclasses.asdict(d) for d in data])
