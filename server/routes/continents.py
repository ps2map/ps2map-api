"""API routes for PS2 continents/zones."""

import fastapi

from ..interfaces import ContinentInfo

router = fastapi.APIRouter(prefix='/continents')


@router.get('/info', response_model=list[ContinentInfo])
async def continent_info() -> list[ContinentInfo]:
    """Return static continent data.

    This includes properties like the continent name or description.
    API consumers are expected to aggressively cache the returned data
    as they will only change with major game updates.
    """
    return []
