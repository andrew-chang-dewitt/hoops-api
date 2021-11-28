"""Routes under `/balance`."""

from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter

from src.config import Config
from src.database import Client
from src.models import Balance, BalanceModel as Model
from src.security import create_auth_dep


def create_balance(config: Config, database: Client) -> APIRouter:
    """Create a balance router & model with access to the given database."""
    # setup db & Balance model
    model = Model(database)
    # setup User auth dependency
    auth_user = create_auth_dep(database, config.jwt_key)

    # setup router
    balance = APIRouter(prefix="/balance", tags=["Balance"])

    @balance.get(
        "/total",
        response_model=Balance,
        summary="Get sum total Balance of all accounts for the current User."
    )
    async def get_root(user_id: UUID = Depends(auth_user)) -> Balance:
        return await model.read.all_by_user(user_id)

    @balance.get(
        "/account/{account_id}",
        response_model=Balance,
        summary="Get the Balance for the given account.",
    )
    async def get_account(
        account_id: UUID,
        user_id: UUID = Depends(auth_user)
    ) -> Balance:
        return await model.read.one_by_account(account_id, user_id)

    return balance
