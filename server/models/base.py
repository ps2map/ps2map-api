"""Data model definitions for map bases and related payloads."""

import typing

from ._model import Field, FrozenModel


class Base(FrozenModel):
    """Static base information.

    This contains unchanging properties of a base, such as its name,
    location on the map, continent, and type. These values generally
    only changes with major game updates and should be heavily cached
    by API consumers.
    """

    id: int = Field(
        title='ID',
        description='The ID of the base. Unique across all continents.',
        example=2306)
    continent_id: int = Field(
        title='Continent ID',
        description='The ID of the continent the base is located on.',
        example=2)
    name: str = Field(
        title='Name',
        description='The name of the base.',
        example='The Crown')
    map_pos: list[float] = Field(
        title='Map Position',
        description='The position of the base on the map in the form '
                    '[x, y]. This uses map coordinates, with the origin in '
                    'the centre of the map, and the positive x-axis pointing '
                    'east, and the positive y-axis pointing north.',
        example=[305.3803, -130.915])
    type_id: int = Field(
        title='Type ID',
        description='The ID of the base type.',
        example=5)
    type_name: str = Field(
        title='Type Name',
        description='The name of the base type.',
        example='Large Outpost')
    resource_capture_amount: float = Field(
        title='Outfit Capture Resources',
        description='The amount of resources awarded to outfits upon '
                    'capturing this base.',
        example=2)
    resource_control_amount: float = Field(
        title='Outfit Control Resources',
        description='The amount of resources awarded to outfits for each '
                    'minute they control this base.',
        example=0.4)
    resource_name: typing.Optional[str] = Field(
        title='Resource Name',
        description='The name of the resource rewarded for controlling this '
                    'base.',
        example='Polystellarite')
    resource_code: typing.Optional[str] = Field(
        title='Resource Asset Code',
        description='A unique string used to identify this resource in source '
                    'code. Provided in case the resource names are localized '
                    'in the future.',
        example='polystellarite')
