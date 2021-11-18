"""Routes under `/account`."""

from typing import List
from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter

from src.database import Client
from src.models import (
    AccountIn,
    AccountNew,
    AccountOut,
    AccountModel as Model,
)
from src.security import get_active_user


class AccountRoutes:
    """Route handlers for `/account`."""

    def __init__(self, model: Model) -> None:
        self.model = model

    async def post(
        self,
        new_account: AccountIn,
        user_id: UUID = Depends(get_active_user)
    ) -> AccountOut:
        """Create a new account for given User."""
        return await self.model.create.new(
            AccountNew(**new_account.dict(), user_id=user_id))

    async def get(
        self,
        user_id: UUID = Depends(get_active_user)
    ) -> List[AccountOut]:
        """Read all accounts for given User."""
        return await self.model.read.many_by_user(user_id=user_id)


def create_account(database: Client) -> APIRouter:
    """Create a account router & model with access to the given database."""
    # setup db & User model
    model = Model(database)
    # set up account router
    routes = AccountRoutes(model)
    account = APIRouter(prefix="/account", tags=["Account"])

    # add routes
    account.post(
        "/",
        response_model=AccountOut,
        summary="Create a new Account for the currently authenticated User."
    )(routes.post)

    account.get(
        "/",
        response_model=List[AccountOut],
        summary="Get the Accounts for the currently authenticated User."
    )(routes.get)

    # return router
    return account
