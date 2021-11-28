"""DB Model for Balance objects."""

from db_wrapper.client import AsyncClient
from db_wrapper.model import (
    sql,
    AsyncRead,
    AsyncModel,
)

from src.models.amount import Amount
from src.models.base import Base


class Balance(Base):
    """Balance information."""

    amount: Amount
    collection: str  # the name of the list of Transactions
    # this Balance is associated with


class BalanceModel:
    """Database queries for Balance objects."""

    client: AsyncClient

    def __init__(self, client: AsyncClient) -> None:
        self.client = client
