"""Routes under `/token`."""

from db_wrapper.model.base import NoResultFound
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from src.database import Client
from src.models import (
    UserOut,
    UserModel as Model,
    Token
)
from src.security import encode_token, CredentialsException


class TokenRoutes:  # pylint: disable=R0903
    """Route handlers for `/token`."""

    model: Model

    def __init__(self, model: Model) -> None:
        self.model = model

    async def post(
        self,
        form_data: OAuth2PasswordRequestForm = Depends()
    ) -> Token:
        """POST `/token` handler."""
        # get user by username & password, return token if auth'd
        # send 401 Unauthorized if model returns no result
        try:
            user: UserOut = await self.model.read.authenticate(
                handle=form_data.username, password=form_data.password)
        except NoResultFound as exc:
            raise CredentialsException() from exc

        token = encode_token(user_id=user.id)

        return Token(access_token=token)

        # check token Dependency?
        # FIXME: maybe this goes in another file & Token models go elsewhere too?
        # decode token
        # return payload


def create_token(database: Client) -> APIRouter:
    """Create a token router & model with access to the given database."""
    # setup db & User model
    model = Model(database)
    # set up token router
    routes = TokenRoutes(model)
    token = APIRouter(prefix="/token")

    # add post_token route
    token.post(
        "/",
        response_model=Token
    )(routes.post)

    # return router
    return token
