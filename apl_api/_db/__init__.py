"""Database abstraction module for the API host.

This module exposes asynchronous getter methods to use in place of
actual database interactions. This both allows changes to the database
without interfering with the API, and it also provides a convenient
hook to add caching and other optimisations down the line
"""

from ._queries import get_continents, get_servers

__all__ = [
    'get_continents',
    'get_servers'
]
