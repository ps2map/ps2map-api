"""Method interfaces for all database interactions.

This module is the only one that should contain any raw SQL.
"""

from typing import List

import asyncpg

from ..interfaces import ContinentInfo, ServerInfo


async def get_continents(pool: asyncpg.pool.Pool) -> List[ContinentInfo]:
    conn: asyncpg.Connection
    async with pool.acquire() as conn:  # type: ignore
        rows = await conn.fetch(  # type: ignore
            '''--sql
            SELECT
                ("id", "name")
            FROM
                "autopl"."Continent"
            ;''')
    return [ContinentInfo(*tuple(r)[0]) for r in rows]  # type: ignore


async def get_servers(pool: asyncpg.pool.Pool) -> List[ServerInfo]:
    conn: asyncpg.Connection
    async with pool.acquire() as conn:  # type: ignore
        rows = await conn.fetch(  # type: ignore
            '''--sql
            SELECT
                ("id", "name", "region")
            FROM
                "autopl"."Server"
            ;''')
    return [ServerInfo(*tuple(r)[0]) for r in rows]  # type: ignore
