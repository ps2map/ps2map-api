"""Root API endpoint.

This might host a usage guide or other documentation at some point.
"""

import fastapi
from starlette.responses import JSONResponse

router = fastapi.APIRouter()


@router.get('/')  # type: ignore
async def root() -> JSONResponse:
    """Default endpoint for empty query."""
    return JSONResponse({'Welcome': 'Nothing to be seen here'})
