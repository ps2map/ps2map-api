"""API routes for PS2 continents/zones."""

import fastapi
from fastapi.params import Query

from ..interfaces import ContinentInfo, ContinentStatus
from ..types import ServerId

router = fastapi.APIRouter(prefix='/continents')


@router.get('/info', response_model=list[ContinentInfo])
async def continent_info() -> list[ContinentInfo]:
    """Return static continent data.

    This includes properties like the continent name or description.
    API consumers are expected to aggressively cache the returned data
    as they will only change with major game updates.
    """
    return []


@router.get('/status', response_model=list[ContinentStatus])
async def continent_status(
    server_id: ServerId = Query(  # type: ignore
        ...,
        title='Server ID',
        description='Unique identifier of the server for which to return a '
        'continent status digest.'
    )
) -> list[ContinentStatus]:
    """Return a momentary status digest for all continents.

    This endpoint will likely be moved to or replicated in a WebSocket
    endpoint in future versions.
    """
    data: list[ContinentStatus] = []
    return data
