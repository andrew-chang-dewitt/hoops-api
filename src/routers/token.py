"""Routes under `/token`."""

from db_wrapper.model.base import NoResultFound
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from src.config import Config
from src.database import Client
from src.models import (
    UserOut,
    UserModel as Model,
    Token
)
from src.security import encode_token, CredentialsException


def create_token(config: Config, database: Client) -> APIRouter:
    """Create a token router & model with access to the given database."""
    # setup db & User model
    model = Model(database)
    # set up token router
    token = APIRouter(prefix="/token", tags=["Authentication"])

    # add post_token route
    @token.post(
        "",
        response_model=Token,
        summary="Get an authentication Token via an OAuth2 Request Form."
    )
    async def post(
        form_data: OAuth2PasswordRequestForm = Depends()
    ) -> Token:
        """POST `/token` handler."""
        # get user by username & password, return token if auth'd
        # send 401 Unauthorized if model returns no result
        try:
            user: UserOut = await model.read.authenticate(
                handle=form_data.username, password=form_data.password)
        except NoResultFound as exc:
            raise CredentialsException() from exc

        token = encode_token(user_id=user.id, key=config.jwt_key)

        return Token(access_token=token)

    # return router
    return token
