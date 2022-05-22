"""Data model definitions for game servers and related payloads."""

import typing

from ._model import Field, FrozenModel


class Server(FrozenModel):
    """Static server information."""

    id: int = Field(
        title='ID',
        description='Unique ID of the server.',
        example=13)
    name: str = Field(
        title='Name',
        description='Canonical name of the continent.',
        example='Cobalt')
    region: str = Field(
        title='Server Region',
        description='Physical location of the game server in the world.\n\n'
                    'This field is only intended for display purposes and is '
                    'neither necessarily accurate nor localized.\n\n'
                    'Note that this field may be localzed in future API '
                    'versions.',
        example='Europe')
    platform: typing.Literal['pc', 'ps4'] = Field(
        title='Server Platform',
        description='Game platform the server is available to.',
        example='pc')
