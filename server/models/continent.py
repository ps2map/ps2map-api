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
    map_size: int = Field(
        title='Map size',
        description='The physical size of the continent in metres.\n\n'
                    'Continents are assumed to be square, so a value of 8192 '
                    'corresponds to a 8192m x 8192m. Note that the actual '
                    'playable area is smaller as this includes the '
                    'out-of-bounds zones along the edges of the map.')


class LatticeLink(FrozenModel):
    """A lattice link between two bases."""

    base_a_id: int = Field(
        title='Base ID',
        description='ID of the first base in the link. This will always be '
                    'the base with the lower ID.',
        example=2402)
    base_b_id: int = Field(
        title='Base ID',
        description='ID of the second base in the link. This will always be '
                    'the base with the higher ID.',
        example=2410)
    map_pos_a_x: float = Field(
        title='Position X',
        description='X position of the first base in the link.',
        example=900.0)
    map_pos_a_y: float = Field(
        title='Position Y',
        description='Y position of the first base in the link.',
        example=-1605.0)
    map_pos_b_x: float = Field(
        title='Position X',
        description='X position of the second base in the link.',
        example=658.5)
    map_pos_b_y: float = Field(
        title='Position Y',
        description='Y position of the second base in the link.',
        example=-1710.0)
