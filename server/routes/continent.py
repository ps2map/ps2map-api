"""API routes for PS2 continents/zones."""

import fastapi

from ..models import Continent

router = fastapi.APIRouter(prefix='/continent')


@router.get('/', response_model=list[Continent])
async def continent() -> list[Continent]:
    """Return static continent data.

    This includes properties like the continent name or description.
    API consumers are expected to aggressively cache the returned data
    as they will only change with major game updates.
    """
    return []
