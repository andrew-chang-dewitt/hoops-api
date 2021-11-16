"""Routes under `/transaction`."""

from uuid import UUID

from fastapi import status as status_code, Body, Depends
from fastapi.routing import APIRouter

from src.security import get_active_user
from src.database import Client
from src.models import (
    UserChanges,
    UserIn,
    UserOut,
    UserModel as Model,
)


class UserRoutes:
    """Route handlers for `/user`."""

    model: Model

    def __init__(self, model: Model) -> None:
        """Bind given Model object to Routes."""
        self.model = model

    async def post_user(self, new_user: UserIn) -> UserOut:
        """Save a new User to the database & return the new information."""
        return await self.model.create.new(new_user)

    async def get_user(self,
                       user_id: UUID = Depends(get_active_user)) -> UserOut:
        """Get the current user's information."""
        return await self.model.read.one_by_id(user_id)

    async def put_user(self,
                       changes: UserChanges,
                       user_id: UUID = Depends(get_active_user)) -> UserOut:
        """Update the current user's information."""
        return await self.model.update.changes(user_id, changes)

    async def put_password(
        self,
        new_password: str = Body(...),
        user_id: UUID = Depends(get_active_user)
    ) -> UserOut:
        """Update the current user's password."""
        return await self.model.update.password(user_id, new_password)

    async def delete_user(
        self,
        user_id: UUID = Depends(get_active_user)
    ) -> UserOut:
        """Delete the current user from the database."""
        return await self.model.delete.one_by_id(str(user_id))


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

    user.get("/", response_model=UserOut)(routes.get_user)

    user.put("/", response_model=UserOut)(routes.put_user)

    user.put("/password", response_model=UserOut)(routes.put_password)

    user.delete("/", response_model=UserOut)(routes.delete_user)

    return user
