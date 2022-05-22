"""API routes for PS2 game servers."""

import fastapi

from ..database import Database, model_factory
from ..models import Server
from ..sql import GET_SERVER_ALL_TRACKED

router = fastapi.APIRouter(prefix='/server')


@router.get('', response_model=list[Server])
async def server() -> list[Server]:
    """Static endpoint returning all tracked servers.

    This endpoint only returns servers that are actively tracked by the
    map API and for which real-time map data is available.
    """
    async with Database().pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(GET_SERVER_ALL_TRACKED)
            bases = await cur.fetchall()
    return [model_factory(Server, b) for b in bases]
