"""Router for `/transaction`."""

from typing import List, Optional
from uuid import UUID

from db_wrapper.model.base import NoResultFound
from fastapi import status, HTTPException, Query
from fastapi.routing import APIRouter

from src.database import Client
from src.models import (
    TransactionBase,
    TransactionDB,
    TransactionModel as Model,
)


class TransactionRoutes:
    """Route handlers for `/transaction`."""

    model: Model

    def __init__(self, model: Model) -> None:
        self.model = model

    async def post_one(self, tran: TransactionBase) -> TransactionDB:
        """Create a new Transaction from the given data."""
        return await self.model.create.one(tran)

    async def get_one(self, tran_id: UUID) -> TransactionDB:
        """Get a single Transaction by it's unique ID."""
        try:
            return await self.model.read.one_by_id(tran_id)
        except NoResultFound as err:
            # NoResultFound should be shown to the user as 404
            raise HTTPException(
                404, f"Transaction with id {tran_id} not found.") from err

    async def put_one(
        self,
        tran_id: UUID,
        updates: TransactionBase
    ) -> TransactionDB:
        """Update a specific transaction with the given data."""
        try:
            return await self.model.update.one_by_id(str(tran_id),
                                                     updates.dict())
        except NoResultFound as err:
            # NoResultFound should be shown to the user as 404
            raise HTTPException(
                404, f"Transaction with id {tran_id} not found.") from err

    async def get_many(
        self,
        limit: Optional[int] = Query(None, gt=0),
        page: Optional[int] = Query(None, ge=0),
    ) -> List[TransactionDB]:
        """Get a list of Transactions, sorted by timestamp (newest first)."""
        result = await self.model.read.many(limit, page)

        if result:
            return result

        # an empty list should be shown to the user as a 404
        raise HTTPException(
            404,
            f"No Transactions found with limit of {limit} on page {page}.")


def create_transaction(database: Client) -> APIRouter:
    """Create a transaction router that uses the given Transaction model."""
    model = Model(database)
    routes = TransactionRoutes(model)

    transaction = APIRouter(prefix="/transaction")

    # Defining my routes by currying APIRouter.<method> & routes.<route>
    # allows me to separate my route handler definition from my route
    # definition. This makes the route handler easier to test independent
    # of the framework.
    transaction.post(
        "/one",
        status_code=status.HTTP_201_CREATED,
        response_model=TransactionDB)(routes.post_one)
    # Alternatively, routes could be defined using APIRouter.add_api_route
    # and specifying the method in an arg (see below), but this is less
    # verbose, and I think easier to read.
    # transaction.add_api_route(
    #     "/one",
    #     routes.post_one,
    #     methods = ["POST"]
    #     status_code = status.HTTP_201_CREATED,
    #     response_model = TransactionDB)

    transaction.get(
        "/one/{tran_id}",
        response_model=TransactionDB)(routes.get_one)

    transaction.put(
        "/one/{tran_id}",
        response_model=TransactionDB)(routes.put_one)

    transaction.get(
        "/many/",
        response_model=List[TransactionDB])(routes.get_many)

    return transaction
