"""Database singleton to manage the database connections for the API.

This is the only real alternative to using SQLAlchemy, which is a bit
overkill for the purposes of this project.
"""

import typing

import psycopg
import psycopg_pool


T = typing.TypeVar('T')

# Type Aliases
Connection = psycopg.AsyncConnection[T]
Cursor = psycopg.AsyncCursor[T]
Pool = psycopg_pool.AsyncConnectionPool


class Database:
    """Singleton for storing the global database connection pool.

    Upon initialization, the :meth:`create_pool` class method must be
    called to set up the pool before it can be used elsewhere.
    """

    __instance: 'Database | None' = None
    _pool: Pool | None

    def __new__(cls) -> 'Database':
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    @property
    def pool(self) -> Pool:
        """The connection pool."""
        if self._pool is None:
            raise RuntimeError('Pool not initialized, run create_pool first')
        return self._pool

    @classmethod
    def create_pool(cls, host: str, port: int, user: str, password: str,
                    database: str) -> None:
        """Create a new connection pool to the database.

        Args:
            host: Hostname of the database server.
            port: Port of the database server.
            user: Username to connect to the database.
            password: Password to connect to the database.
            database: Name of the database to connect to.

        """
        connection_string = (f'host={host} '
                             f'port={port} '
                             f'user={user} '
                             f'password={password} '
                             f'dbname={database}')
        cls._pool = psycopg_pool.AsyncConnectionPool(connection_string)
