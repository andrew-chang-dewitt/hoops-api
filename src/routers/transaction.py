"""Transaction router."""

from typing import List
from uuid import UUID

from fastapi import status as status_code, Depends
from fastapi.routing import APIRouter

from src.config import Config
from src.database import Client
from src.models import (
    TransactionIn,
    TransactionOut,
    TransactionChanges,
    TransactionModel as Model,
    AccountModel,
)
from src.security import create_auth_dep, CredentialsException


def create_transaction(config: Config, database: Client) -> APIRouter:
    """Create transaction router & model with access to the given database."""
    # setup db & Transaction model
    model = Model(database)
    account_model = AccountModel(database)
    # setup User authentication dependency
    auth_user = create_auth_dep(database, config.jwt_key)

    transaction = APIRouter(prefix="/transaction", tags=["Transaction"])

    @transaction.post(
        "",
        response_model=TransactionOut,
        status_code=status_code.HTTP_201_CREATED,
        summary="Create a new Transaction for the given Account.",
    )
    async def post_root(
        new_tran: TransactionIn,
        user_id: UUID = Depends(auth_user),
    ) -> TransactionOut:
        """Save given Transaction to database."""
        # check user authorized for adding to given account
        account = await account_model.read.one_by_id(new_tran.account_id)

        try:
            assert account.user_id == user_id
        except AssertionError as exc:
            raise CredentialsException from exc

        return await model.create.new(new_tran)

    @transaction.get(
        "",
        response_model=List[TransactionOut],
        summary="Fetch all Transactions for the authenticated User.",
    )
    async def get_root(
        user_id: UUID = Depends(auth_user)
    ) -> List[TransactionOut]:
        """Get all Transactions."""
        return await model.read.many_by_user(user_id)

    @transaction.put(
        "/{transaction_id}",
        response_model=TransactionOut,
        summary="Edit the given Transaction.")
    async def put_id(
        transaction_id: UUID,
        changes: TransactionChanges,
        user_id: UUID = Depends(auth_user),
    ) -> TransactionOut:
        """Edit the given user."""
        tran = await model.read.one_by_id(transaction_id)
        account = await account_model.read.one_by_id(tran.account_id)

        try:
            assert account.user_id == user_id
        except AssertionError as exc:
            raise CredentialsException from exc

        return await model.update.changes(transaction_id, changes)

    return transaction
