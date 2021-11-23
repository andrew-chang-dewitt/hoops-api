"""Routes under `/transaction`."""

from uuid import UUID

from fastapi import status as status_code, Body, Depends
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from psycopg2.errors import UniqueViolation  # pylint: disable=E0611

from src.config import Config
from src.database import Client
from src.models import (
    UserChanges,
    UserIn,
    UserOut,
    UserModel as Model,
)
from src.security import create_auth_dep


def create_user(config: Config, database: Client) -> APIRouter:
    """Create a user router & model with access to the given database."""
    # setup db & User model
    model = Model(database)
    # setup User authentication dependency
    auth_user = create_auth_dep(database, config.jwt_key)

    user = APIRouter(prefix="/user", tags=["User"])

    @user.post(
        "",
        status_code=status_code.HTTP_201_CREATED,
        response_model=UserOut,
        summary="Create a new User.")
    async def post_user(new_user: UserIn) -> UserOut:
        """Save a new User to the database & return the new information."""
        try:
            return await model.create.new(new_user)
        except UniqueViolation as exc:
            raise HTTPException(
                409,
                detail=f"User with handle {new_user.handle} already exists."
            ) from exc

    @user.get(
        "",
        response_model=UserOut,
        summary="Get the currently authenticated User.")
    async def get_user(user_id: UUID = Depends(auth_user)) -> UserOut:
        """Get the current user's information."""
        return await model.read.one_by_id(user_id)

    @user.put(
        "",
        response_model=UserOut,
        summary="Update the currently authenticated User's information.")
    async def put_user(changes: UserChanges,
                       user_id: UUID = Depends(auth_user)) -> UserOut:
        """Update the current user's information."""
        return await model.update.changes(user_id, changes)

    @user.put(
        "/password",
        response_model=UserOut,
        summary="Update the currently authenticated User's password.")
    async def put_password(new_password: str = Body(...),
                           user_id: UUID = Depends(auth_user)) -> UserOut:
        """Update the current user's password."""
        result = await model.update.password(user_id, new_password)
        print("put_password result:", result)

        return result

    @user.delete(
        "",
        response_model=UserOut,
        summary="Delete the currently authenticated User.")
    async def delete_user(user_id: UUID = Depends(auth_user)) -> UserOut:
        """Delete the current user from the database."""
        return await model.delete.one_by_id(str(user_id))

    return user
