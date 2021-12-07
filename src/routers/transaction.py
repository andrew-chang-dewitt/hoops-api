"""Transaction router."""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from fastapi import status as status_code, Depends, Query
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
from src.models.filters import (
    equals,
    greater_than_or_equal_to,
    less_than_or_equal_to,
    logical_and,
)
from src.routers.helpers.filters import a_b_both_or_none
from src.security import create_auth_dep, UnauthorizedException


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
        summary="Create a new Transaction for the given Account.")
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
            raise UnauthorizedException from exc

        return await model.create.new(new_tran)

    default_limit = Query(
        50,
        description="Only return specified number of Transactions.")
    default_page = Query(
        0,
        description="Return given page of Transactions.")
    default_sort = Query(
        "timestamp",
        description="Sort Transactions by given column.")
    default_account_id = Query(
        None,
        description="Only return Transactions belonging to this Account.")
    default_payee = Query(
        None,
        description="Only return Transactions with matching payee.")
    default_minimum_amount = Query(
        None,
        description="Only return Transactions greater than or equal to amount."
    )
    default_maximum_amount = Query(
        None,
        description="Only return Transactions less than or equal to amount.")
    default_after = Query(
        None,
        description="Only return Transactions after the given date & time.")
    default_before = Query(
        None,
        description="Only return Transactions before the given date & time.")

    @transaction.get(
        "",
        response_model=List[TransactionOut],
        summary="Fetch all Transactions for the authenticated User.")
    async def get_root(
        user_id: UUID = Depends(auth_user),
        account_id: Optional[UUID] = default_account_id,
        payee: Optional[str] = default_payee,
        minimum_amount: Optional[Decimal] = default_minimum_amount,
        maximum_amount: Optional[Decimal] = default_maximum_amount,
        after: Optional[datetime] = default_after,
        before: Optional[datetime] = default_before,
        limit: Optional[int] = default_limit,
        page: Optional[int] = default_page,
        sort: Optional[str] = default_sort,
    ) -> List[TransactionOut]:
        """Get all Transactions."""
        amount = a_b_both_or_none(minimum_amount,
                                  maximum_amount,
                                  greater_than_or_equal_to,
                                  less_than_or_equal_to,
                                  logical_and)
        timestamp = a_b_both_or_none(after,
                                     before,
                                     greater_than_or_equal_to,
                                     less_than_or_equal_to,
                                     logical_and)

        return await model.read.many_by_user(
            user_id,
            # mypy can't tell these have default values given by Query
            limit=limit,  # type: ignore
            page=page,  # type: ignore
            sort=sort,  # type: ignore
            account_id=equals(account_id),
            payee=equals(payee),
            amount=amount,
            timestamp=timestamp)

    @transaction.put(
        "/{transaction_id}",
        response_model=TransactionOut,
        summary="Edit the given Transaction.")
    async def put_id(
        transaction_id: UUID,
        changes: TransactionChanges,
        user_id: UUID = Depends(auth_user),
    ) -> TransactionOut:
        """Edit the given Transaction."""
        tran = await model.read.one_by_id(transaction_id)
        account = await account_model.read.one_by_id(tran.account_id)

        try:
            assert account.user_id == user_id
        except AssertionError as exc:
            raise UnauthorizedException from exc

        return await model.update.changes(transaction_id, changes)

    @transaction.delete(
        "/{transaction_id}",
        response_model=TransactionOut,
        summary="Delete the given Transaction.")
    async def delete_id(
        transaction_id: UUID,
        user_id: UUID = Depends(auth_user),
    ) -> TransactionOut:
        """Delete the given Transaction."""
        tran = await model.read.one_by_id(transaction_id)
        account = await account_model.read.one_by_id(tran.account_id)

        try:
            assert account.user_id == user_id
        except AssertionError as exc:
            raise UnauthorizedException from exc

        return await model.delete.one_by_id(str(transaction_id))

    @transaction.put(
        "/{transaction_id}/spent_from/{spent_from_id}",
        response_model=TransactionOut,
        summary="Mark Transaction as \"spent from\" the given Envelope")
    async def put_spent_from(
        transaction_id: UUID,
        spent_from_id: UUID,
        user_id: UUID = Depends(auth_user),
    ) -> TransactionOut:
        """Mark Transaction as Spent From given Envelope."""
        tran = await model.read.one_by_id(transaction_id)
        account = await account_model.read.one_by_id(tran.account_id)

        try:
            assert account.user_id == user_id
        except AssertionError as exc:
            raise UnauthorizedException from exc

        return await model.update.changes(transaction_id,
                                          TransactionChanges(
                                              spent_from=spent_from_id))

    return transaction
