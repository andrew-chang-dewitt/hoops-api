"""Transaction router."""

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

    return transaction
