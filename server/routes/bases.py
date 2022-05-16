"""API routes for map bases."""

import fastapi
from fastapi.params import Query

from ..interfaces import BaseInfo, BaseStatus
from ..types import BaseId, ContinentId, ServerId

router = fastapi.APIRouter(prefix='/bases')


@router.get('/info', response_model=list[BaseInfo])
async def base_info(
    continent_id: BaseId = Query(  # type: ignore
        ...,
        title='Continent ID',
        description='Unique identifier of the continent for which to return '
        'base information.'),
) -> list[BaseInfo]:
    """Return the list of bases for a given continent.

    This payload contains unchanging properties like the base name or
    type. API consumers are expected to aggressively cache the returned
    data as they will only change with major game updates.
    """
    data: list[BaseInfo] = []
    if not data:
        msg = f'No bases found for continent ID: {continent_id}'
        raise fastapi.HTTPException(status_code=404, detail=msg)
    return data


@router.get('/status', response_model=list[BaseStatus])
async def base_status(
    continent_id: ContinentId = Query(  # type: ignore
        ...,
        title='Continent ID',
        description='Unique identifier of the continent for which to return '
        'a base status digest.'),
    server_id: ServerId = Query(  # type: ignore
        ...,
        title='Server ID',
        description='Unique identifier of the server for which to return a '
        'base status digest.')
) -> list[BaseStatus]:
    """Return a momentary status digest for all bases on a continent.

    This endpoint will likely be moved to or replicated in a WebSocket
    endpoint in future versions.
    """
    data: list[BaseStatus] = []
    if not data:
        msg = f'No bases found for continent ID: {continent_id}'
        raise fastapi.HTTPException(status_code=404, detail=msg)
    return data
