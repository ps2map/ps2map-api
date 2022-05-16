"""Data model definitions for continents/zones and related payloads."""

from ._model import Field, FrozenModel


class ContinentInfo(FrozenModel):
    """Static continent information.

    This contains unchanging properties of a continent such as its
    name, a human-friendly description, asset codes, and size. These
    values generally only changes with major game updates and should be
    heavily cached by API consumers.
    """

    id: int = Field(
        title='ID',
        description='The ID of the continent.',
        example=344)
    name: str = Field(
        title='Name',
        description='The name of the continent.',
        example='Oshur')
    code: str = Field(
        title='Asset code',
        description='A unique string used to identify this continent in '
                    'source code. Provided in case the continent names are '
                    'localized in the future.',
        example='oshur')
    description: str = Field(
        title='Description',
        description='A human-friendly description of the continent intended '
                    'for use as flavour-text in continent selection screens.',
        example='The tropical isles of Oshur are reminiscent of a time before '
                'the Auraxian war, where research and exploration were the '
                'most valued pursuits, and the factions weren\'t fully '
                'divided.')
