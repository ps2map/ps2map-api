"""Factory methods for creating pydantic Model instance from DB data.

This module is tied to the database layout, the SQL commands, and the
pydantic Model classes themselves.
"""

import typing

import pydantic

from ..models import Base, Continent, Server

__all__ = [
    'model_factory',
]

_ModelTypes = Base | Continent | Server
_Model = typing.TypeVar('_Model', bound=_ModelTypes)


def model_factory(klass: type[_Model], row: tuple[typing.Any, ...]) -> _Model:
    """Create a pydantic Model instance from a DB row."""
    assert issubclass(klass, pydantic.BaseModel)    # pylint: disable=no-member

    # NOTE: This uses "is" to compare classes as subclasses are not meant to
    # pass these checks. Pydantic subclasses would introduce additional fields,
    # for which the parser would not work.
    if klass is Base:
        row_list = list(row)
        map_pos = [float(row_list.pop(3)) for _ in range(2)]
        row_list.insert(3, map_pos)
        row = tuple(row_list)

    return klass(**dict(zip(klass.__fields__, row)))
