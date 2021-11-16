"""Security constants & methods."""

from datetime import datetime, timedelta
import os
from typing import cast, Dict
from uuid import UUID

from dotenv import load_dotenv
from fastapi import status as status_code, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

load_dotenv(".secrets")
SECRET_KEY = os.getenv("APP_KEY")
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


def encode_token(user_id: UUID) -> str:
    """Encode & return a new JWT containing the given ID."""
    data = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }

    # FIXME: python-jose has no typing & jwt.encode returns Any
    # casting to str to allow typing downstream for now instead of
    # creating stubs, see https://github.com/mpdavis/python-jose/pull/265
    # for open PR that adds typing
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return cast(str, token)


def get_active_user(token: str = Depends(oauth2_scheme)) -> UUID:
    """Get current user ID from token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise CredentialsException()
    except JWTError as err:
        raise CredentialsException() from err

    return UUID(user_id)
