"""Main ASGI application hosting the API.

This is imported and run directly by the uvicorn server, which must
reside in its own thread.

None of the contents of this module are meant to be exported or used in
other modules; this is the main client.
"""

import logging

import fastapi
from fastapi.middleware.cors import CORSMiddleware

from . import endpoints
from ._logging import ForwardHandler

# List of remote hosts for which CORS reponses headers should be included
_ORIGINS = [
    '*'
]

# Customise logging behaviour
_api_log = logging.getLogger('api.server')
_uvicorn_log = logging.getLogger('uvicorn')
_uvicorn_log.handlers = [ForwardHandler(_api_log)]

# Create the API application
app = fastapi.FastAPI()

# Add CORS middleware to inject appropriate response headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=_ORIGINS)

# NOTE: The fragmentation of the endpoints is mostly to simplify adaptions, it
# has a neglegible performance impact upon startup and is just as speedy as a
# monolithic API application once it's set up and running.

# Register the different path routers for the various endpoints
for name in endpoints.__all__:
    router = getattr(endpoints, name)
    app.include_router(router)
