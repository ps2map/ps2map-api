"""Database abstraction module for the API host.

This module exposes asynchronous getter methods to use in place of
actual database interactions. This both allows changes to the database
without interfering with the API, and it also provides a convenient
hook to add caching and other optimisations down the line
"""

import os
from typing import Optional, cast

import asyncpg

from ._queries import get_continents, get_servers

__all__ = [
    'get_continents',
    'get_servers',
    'get_pool'
]

# Default database configuration
DEFAULT_DB_HOST = '127.0.0.1'
DEFAULT_DB_NAME = 'postgres'
DEFAULT_DB_USER = 'postgres'

# Global pool instance
_pool: Optional[asyncpg.pool.Pool] = None


async def get_pool() -> asyncpg.pool.Pool:
    """Global pool instance accessor method.

    This method is called by the FastAPI dependency system to pass the
    global asyncpg pool instance to each router and path operation as
    required.
    """
    global _pool
    if _pool is None:
        db_name = os.getenv('_DB_NAME', DEFAULT_DB_NAME)
        db_host = os.getenv('_DB_HOST', DEFAULT_DB_HOST)
        db_user = os.getenv('_DB_USER', DEFAULT_DB_USER)
        db_pass = os.getenv('_DB_PASS')
        if db_pass is None:
            raise RuntimeError('No database password specified,'
                               'unable to connect')
        _pool = asyncpg.create_pool(  # type: ignore
            user=db_user, password=db_pass, database=db_name, host=db_host)
        # Initialise connection pool
        await _pool  # type: ignore
    return cast(asyncpg.pool.Pool, _pool)
