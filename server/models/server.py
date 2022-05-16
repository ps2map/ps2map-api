"""Data model definitions for game servers and related payloads."""

import typing

from ._model import Field, FrozenModel


class ServerInfo(FrozenModel):
    """Static server information.

    This contins unchanging properties of a server such as its name or
    region. These values generally only change with server mergers or
    other major infrastructure changes and should be heavily cached by
    API consumers.
    """

    id: int = Field(
        title='ID',
        description='The ID of the server.',
        example=13)
    name: str = Field(
        title='Name',
        description='The name of the server.',
        example='Cobalt')
    region: str = Field(
        title='Server Region',
        description='Physical location of the game server in the world.',
        example='Europe')
    platform: typing.Literal['pc', 'ps4'] = Field(
        title='Server Platform',
        description='Game platform the server is available to.',
        example='pc')
