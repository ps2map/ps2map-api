"""API routes for PS2 game servers."""

import fastapi

from ..interfaces import ServerInfo

router = fastapi.APIRouter(prefix='/servers')


@router.get('/info', response_model=list[ServerInfo])
async def server_info() -> list[ServerInfo]:
    """Return the list of servers.

    This payload contains unchanging properties like the server name or
    region. API consumers are expected to aggressively cache the
    returned data as they will only change with major game updates.
    """
    return []
