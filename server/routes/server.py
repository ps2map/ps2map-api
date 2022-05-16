"""API routes for PS2 game servers."""

import fastapi

from ..database import Database, model_factory
from ..models import Server

router = fastapi.APIRouter(prefix='/server')


@router.get('', response_model=list[Server])
async def server() -> list[Server]:
    """Return the list of servers.

    This payload contains unchanging properties like the server name or
    region. API consumers are expected to aggressively cache the
    returned data as they will only change with major game updates.
    """
    async with Database().pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute('SELECT "id", "name", "region", "platform" '
                              'FROM "API_static"."Server";')
            bases = await cur.fetchall()
    return [model_factory(Server, b) for b in bases]
