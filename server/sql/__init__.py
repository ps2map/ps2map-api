"""Loads SQL commands from disk and stores them for later access."""

import pathlib

__all__ = [
    'GET_BASE_BY_CONTINENT',
    'GET_BASE_STATUS',
    'GET_CONTINENT_ALL',
    'GET_CONTINENT_ALL_TRACKED',
    'GET_LATTICE_BY_CONTINENT',
    'GET_SERVER_ALL_TRACKED',
]

# Relative directory to the SQL files
_SQL_DIR = pathlib.Path(__file__).parent


def _get_sql(filename: str) -> str:
    """Loads a file from disk and returns its contents."""
    with open(_SQL_DIR / filename, encoding='utf-8') as sql_file:
        return sql_file.read()


GET_BASE_BY_CONTINENT = _get_sql('get_Base_byContinent.sql')
GET_BASE_STATUS = _get_sql('get_BaseStatus.sql')
GET_CONTINENT_ALL = _get_sql('get_Continent_all.sql')
GET_CONTINENT_ALL_TRACKED = _get_sql('get_Continent_allTracked.sql')
GET_LATTICE_BY_CONTINENT = _get_sql('get_Lattice_byContinent.sql')
GET_SERVER_ALL_TRACKED = _get_sql('get_Server_allTracked.sql')
