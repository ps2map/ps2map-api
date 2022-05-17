"""Data model definitions for continents/zones and related payloads."""

from ._model import Field, FrozenModel


class Continent(FrozenModel):
    """Static continent information."""

    id: int = Field(
        title='ID',
        description='Unique ID of the continent.\n\n'
                    'For most continents, this ID is the same as the IDs used '
                    'for *zone* entries in the game. However, this is not a '
                    'guarantee and may change between API versions.',
        example=344)
    name: str = Field(
        title='Name',
        description='Canonical name of the continent.',
        example='Oshur')
    code: str = Field(
        title='Asset code',
        description='A unique string designed to identify continent assets in '
                    'client code.',
        example='oshur')
    description: str = Field(
        title='Description',
        description='A human-friendly description of the continent primarily '
                    'intended for use as flavour-text in continent selection '
                    'screens.',
        example='The tropical isles of Oshur are reminiscent of a time before '
                'the Auraxian war, where research and exploration were the '
                'most valued pursuits, and the factions weren\'t fully '
                'divided.')


class LatticeLink(FrozenModel):
    """A lattice link between two bases."""

    base_id_a: int = Field(
        title='Base ID',
        description='ID of the first base in the link. This will always be '
                    'the base with the lower ID.',
        example=2402)
    base_id_b: int = Field(
        title='Base ID',
        description='ID of the second base in the link. This will always be '
                    'the base with the higher ID.',
        example=2410)
