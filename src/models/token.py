"""Token data Models."""

from uuid import UUID

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Token(BaseModel):  # pylint: disable=R0903
    """Token fields."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):  # pylint: disable=R0903
    """Token payload."""

    user_id: UUID
