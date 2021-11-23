"""Shared Model behavior."""

from pydantic import (  # pylint: disable=no-name-in-module
    BaseModel,
)
from db_wrapper.model import ModelData


class Base(BaseModel):
    """Shared Model behavior."""

    class Config:
        """Configure all Models' Pydantic features."""

        # will now throw validation error if extra fields are given
        extra = "forbid"


class BaseDb(Base, ModelData):
    """Combine shared Pydantic settings & required id field."""
