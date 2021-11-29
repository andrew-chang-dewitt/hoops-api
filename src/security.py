"""Security constants & methods."""

from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable, Protocol
from uuid import UUID

from db_wrapper.model.base import NoResultFound
from fastapi import status as status_code, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.database import Client
from src.models import UserModel


ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class CredentialsException(HTTPException):
    """Throw when unable to process a user's credentials."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status_code.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UnauthorizedException(HTTPException):
    """Throw when unable to process a user's credentials."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status_code.HTTP_403_FORBIDDEN,
            detail="User not authorized for method on requested resource",
        )


def encode_token(
    user_id: UUID,
    key: str,
) -> str:
    """Encode & return a new JWT containing the given ID."""
    data = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }

    return jwt.encode(data, key, algorithm=ALGORITHM)  # type: ignore


def create_auth_dep(
    database: Client,
    key: str,
) -> Callable[[str], Awaitable[UUID]]:
    async def auth_user(
        token: str = Depends(oauth2_scheme)
    ) -> UUID:
        """Get current user ID from token."""
        try:
            payload = jwt.decode(token, key, algorithms=[ALGORITHM])
            id_str = payload.get("sub")

            if id_str is None:
                raise CredentialsException()
        except JWTError as err:
            raise CredentialsException() from err

        user_id = UUID(id_str)
        user_model = UserModel(database)

        try:
            await user_model.read.one_by_id(user_id)
        except NoResultFound:
            raise CredentialsException()

        return user_id

    return auth_user
