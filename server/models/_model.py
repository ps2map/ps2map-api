"""Type aliases and base classes for API data models."""

import pydantic


Field = pydantic.Field


class FrozenModel(pydantic.BaseModel):  # pylint: disable=no-member
    """Base class for immutable data models."""

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False
