"""Endpoint definitions for the API."""

from .base import router as base
from .continent import router as continent
from .server import router as server

# NOTE: app.py expects this __all__ export to only contain routers. Non-router
# things will make it very sad.
#
# This is intentional. Add an isinstance check to app.py if you deem non-router
# things in the __all__ list necessary.

__all__ = [
    'base',
    'continent',
    'server'
]
