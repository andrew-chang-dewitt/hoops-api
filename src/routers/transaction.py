"""Transaction router."""

from fastapi import status as status_code, Depends
from fastapi.routing import APIRouter

from src.config import Config
from src.database import Client
from src.models import (
    TransactionIn,
    TransactionOut,
    TransactionModel as Model,
)
from src.security import create_auth_dep


def create_transaction(config: Config, database: Client) -> APIRouter:
    """Create transaction router & model with access to the given database."""
    # setup db & Transaction model
    model = Model(database)
    # setup User authentication dependency
    auth_user = create_auth_dep(database, config.jwt_key)

    transaction = APIRouter(prefix="/transaction", tags=["Transaction"])

    @transaction.post(
        "",
        response_model=TransactionOut,
        status_code=status_code.HTTP_201_CREATED,
        summary="Create a new Transaction for the given Account.",
        # user_id not needed in method, but authorization guard still needed
        dependencies=[Depends(auth_user)]
    )
    async def post_root(new_tran: TransactionIn) -> TransactionOut:
        """Save given Transaction to database."""
        return await model.create.new(new_tran)

    return transaction
