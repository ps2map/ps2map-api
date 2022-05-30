"""Custom StaticFiles app for static files with caching headers."""

from starlette.staticfiles import StaticFiles
from starlette.responses import Response
from starlette.types import Scope

__all__ = [
    'StaticFilesApp'
]

MAX_AGE = 60 * 60 * 24 * 7  # 1 week
CACHE_CONTROL = f'private, max-age={MAX_AGE}, immutable'


class StaticFilesApp(StaticFiles):
    """Custom StaticFiles app for static files with caching headers."""

    async def get_response(self, path: str, scope: Scope) -> Response:
        response = await super().get_response(path, scope)
        # Cache indefinitely, changes should be reflected in the URL without
        # any updates to existing files
        response.headers['Cache-Control'] = CACHE_CONTROL
        return response
