"""Custom types used for the api module.

This mostly covers type hints for modules that do not provide sensible
type hints themselves.

"""

import socket
from typing import Any

from uvicorn.config import Config
from uvicorn.server import ServerState

__all__ = [
    'Server'
]


class Server:
    """Main uvicorn server object."""

    config: Config
    server_state: ServerState
    started: bool
    should_exit: bool
    force_exit: bool
    last_notified: int

    #pylint: disable=unused-argument,unnecessary-ellipsis

    def __init__(self, config: Config) -> None:
        ...

    def run(self, sockets: list[socket.SocketIO] | None = None) -> None:
        """Synchronous wrapper for ``Server.serve()``."""
        ...

    async def serve(self, sockets: list[socket.SocketIO] | None = None
                    ) -> None:
        """Main server hosting routine."""
        ...

    async def startup(self, sockets: list[socket.SocketIO] | None = None
                      ) -> None:
        """Server startup routine."""
        ...

    async def main_loop(self) -> None:
        """Main server execution loop."""
        ...

    async def on_tick(self, counter: int) -> bool:
        """Server tick callback.

        Return whether the server should exit at a given loop.
        """
        ...

    async def shutdown(self, sockets: list[socket.SocketIO] | None = None
                       ) -> None:
        """Server shutdown routine."""
        ...

    def install_signal_handlers(self) -> None:
        """Platform-agmostic signal handler installation."""
        ...

    def handle_exit(self, sig: Any, frame: Any) -> None:
        """Server exit request handler."""
        ...
