"""Data model definitions for map bases and related payloads."""

import datetime
import typing

from ._model import Field, FrozenModel


class Base(FrozenModel):
    """Static base information."""

    id: int = Field(
        title='ID',
        description='Unique ID of the base.\n\n'
                    'For most bases, this ID is the same as the IDs used for '
                    '*map_region* entries in the game. However, this is not '
                    'a guarantee, and the IDs used in this API may change '
                    'between API versions.',
        example=2306)
    continent_id: int = Field(
        title='Continent ID',
        description='Unique ID of the continent the base is located on.\n\n'
                    'As with the *id* field, this value currently matches '
                    'the IDs used for *zone* entries in the game but may '
                    'change between API versions.',
        example=2)
    name: str = Field(
        title='Name',
        description='Canonical name of the base.\n\n'
                    'User-facing name of the base as it appears in-game. Base '
                    'names are not localized and are the same across all '
                    'game locales.\n\n'
                    'Note that primary facilities such as Tech Plants and '
                    'Amp Stations are generally displayed as a combination of '
                    'the base name and type (e.g. "Eisa Tech Plant"). These '
                    'display names are localized in the game, and the '
                    '*type_name* field of this payload may be replaced with a '
                    'localized version in future API versions.',
        example='The Crown')
    map_pos: list[float] = Field(
        title='Map Position',
        description='Position of the base on the map.\n\n'
                    'This field is a list of two numbers, namely the x and y '
                    'coordinates of the base icon on the map. The coordinate '
                    'system used is similar to the one used in the game, but '
                    'with some alterations to naming and coordinate axes.\n\n'
                    'The x-axis is the horizontal axis pointing east, and the '
                    'y-axis is the vertical axis pointing north. The origin '
                    'is at the centre of the map.\n\n'
                    'For a continent with map size 8192, this means that the '
                    'coordinates are in the range [-4096, 4096].\n\n'
                    'Note that this field is always provided, even for bases '
                    'with no actual map icon such as the Shattered Warpgate. '
                    'To determine whether to display a map icon or not, check '
                    'the value of *type_code*.',
        example=[305.3803, -130.915])
    type_name: str = Field(
        title='Base Type Name',
        description='The name of the base type.\n\n'
                    'This field is the display name of the base type. In the '
                    'game, base types are localized strings, and a future '
                    'version of this API may replace this field with a '
                    'localized version to support applications using '
                    'non-English locales.',
        example='Large Outpost')
    type_code: str = Field(
        title='Base Type Code',
        description='Identification code of the base type.\n\n'
                    'A unique string designed to identify base types in '
                    'client code, like for selecting base icon assets.',
        example='large-outpost')
    resource_capture_amount: float = Field(
        title='Capture Resources',
        description='The amount of resources awarded to a player outfit upon '
                    'capturing this base in their name.\n\n'
                    'This field is generally the same across bases of the '
                    'same type, though some bases such as The Crown have '
                    'custom overrides due to their central location.',
        example=2)
    resource_control_amount: float = Field(
        title='Control Resources',
        description='The amount of resources awarded to player outfits for '
                    'each minute they control this base.\n\n'
                    'This field is generally the same across bases of the '
                    'same type, though some bases such as The Crown have '
                    'custom overrides due to their central location.',
        example=0.4)
    resource_name: typing.Optional[str] = Field(
        title='Resource Name',
        description='The name of the outfit resource awarded to outfits for '
                    'capturing or controlling this base.',
        example='Polystellarite')
    resource_code: typing.Optional[str] = Field(
        title='Resource Asset Code',
        description='A unique string designed to identify base types in '
                    'client code.\n\n'
                    'As with base types, resources names may be localized in '
                    'future API versions.',
        example='polystellarite')


class BaseStatus(FrozenModel):
    """Base ownership information."""

    base_id: int = Field(
        title='ID',
        description='Unique ID of the base.',
        example=2203)
    server_id: int = Field(
        title='Server ID',
        description='Unique ID of the server for which the base status is '
        'provided.',
        example=10)
    owning_faction_id: int = Field(
        title='Owning Faction ID',
        description='Unique ID of the faction that owns the base.\n\n'
                    'This field will generally be one of the three primary '
                    'factions, i.e. TR, VC, and NC. NSO cannot currently '
                    'capture bases in their name and will not appear in this '
                    'field.\n\n'
                    'Additionally, this field may be set to 0 for bases for '
                    'which no base ownership information is available, '
                    'generally during API outages or other infrastructure '
                    'issues.\n\n'
                    'Finally, a value of -1 indicates that the base is '
                    'currently unclaimed/disabled, as happens during low-pop '
                    'alerts with reduced base availability.',
        example=2)
    owned_since: datetime.datetime = Field(
        title='Owned Since',
        description='Timestamp of the time the given base was claimed by its '
                    'current owning faction.\n\n'
                    'This field returns a string in ISO 8601 format.',
        example=datetime.datetime.now())
