"""Routes under `/transaction`."""

from uuid import UUID

from fastapi import status as status_code, Depends
from fastapi.routing import APIRouter

from src.security import get_active_user
from src.database import Client
from src.models import (
    UserIn,
    UserOut,
    UserModel as Model,
)


class UserRoutes:
    """Route handlers for `/user`."""

    model: Model

    def __init__(self, model: Model) -> None:
        self.model = model

    async def post_user(self, new_user: UserIn) -> UserOut:
        """Save a new User to the database & return the new information."""
        return await self.model.create.new(new_user)

    async def get_user(self,
                       user_id: UUID = Depends(get_active_user)) -> UserOut:
        return await self.model.read.one_by_id(user_id)


def create_user(database: Client) -> APIRouter:
    """Create a user router & model with access to the given database."""
    model = Model(database)
    routes = UserRoutes(model)

    user = APIRouter(prefix="/user")

    user.post(
        "/",
        status_code=status_code.HTTP_201_CREATED,
        response_model=UserOut
    )(routes.post_user)

    user.get(
        "/",
        response_model=UserOut
    )(routes.get_user)

    return user
