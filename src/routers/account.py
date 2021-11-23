"""Routes under `/account`."""

from typing import List
from uuid import UUID

from fastapi import status as status_code, Depends
from fastapi.routing import APIRouter

from src.config import Config
from src.database import Client
from src.models import (
    AccountChanges,
    AccountIn,
    AccountNew,
    AccountOut,
    AccountModel as Model,
)
from src.security import create_auth_dep


def create_account(config: Config, database: Client) -> APIRouter:
    """Create a account router & model with access to the given database."""
    # setup db & Account model
    model = Model(database)
    # setup User authentication dependency
    auth_user = create_auth_dep(database, config.jwt_key)

    # set up account router
    account = APIRouter(prefix="/account", tags=["Account"])

    # add routes
    @account.post(
        "",
        response_model=AccountOut,
        status_code=status_code.HTTP_201_CREATED,
        summary="Create a new Account for the currently authenticated User.")
    async def post(
        new_account: AccountIn,
        user_id: UUID = Depends(auth_user)
    ) -> AccountOut:
        """Create a new account for given User."""
        return await model.create.new(
            AccountNew(**new_account.dict(), user_id=user_id))

    @account.get(
        "",
        response_model=List[AccountOut],
        summary="Get the Accounts for the currently authenticated User.")
    async def get(
        user_id: UUID = Depends(auth_user)
    ) -> List[AccountOut]:
        """Read all open accounts for given User."""
        return await model.read.many_by_user(user_id=user_id)

    @account.put(
        "/{account_id}",
        response_model=AccountOut,
        summary="Update the given Account."
    )
    async def put_id(
        account_id: UUID,
        changes: AccountChanges,
        user_id: UUID = Depends(auth_user),
    ) -> AccountOut:
        """Update the given account with the given changes."""
        return await model.update.changes(account_id, user_id, changes)

    @account.put(
        "/{account_id}/closed",
        response_model=AccountOut,
        summary="Mark the given Account as closed."
    )
    async def put_closed(
        account_id: UUID,
        user_id: UUID = Depends(auth_user),
    ) -> AccountOut:
        """Mark the given account as closed."""
        return await model.update.changes(
            account_id,
            user_id,
            AccountChanges(closed=True))

    @account.get(
        "/closed",
        response_model=List[AccountOut],
        summary="Get all closed Accounts for current User."
    )
    async def get_closed(
        user_id: UUID = Depends(auth_user),
    ) -> List[AccountOut]:
        """Mark the given account as closed."""
        return await model.read.many_by_user(
            user_id, closed=True)

    # return router
    return account
