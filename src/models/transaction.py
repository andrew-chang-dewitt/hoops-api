"""DB Model for Transaction objects."""

from datetime import datetime
from uuid import UUID

from db_wrapper.client import AsyncClient
from db_wrapper.model import (
    AsyncModel
)
from pydantic import ConstrainedDecimal  # pylint: disable=E0611

from src.models.base import Base, BaseDb


class Amount(ConstrainedDecimal):
    """A Decimal, constrained to 2 decimal places."""

    # pylint: disable=too-few-public-methods

    decimal_places = 2


class TransactionBase(Base):
    """Base Transaction fields."""

    amount: Amount
    description: str
    payee: str
    timestamp: datetime
    account_id: UUID


class TransactionIn(TransactionBase):
    """Fields used when creating a new Transaction."""

    # simply a copy of TransactionBase for now


class TransactionOut(TransactionBase, BaseDb):
    """Fields used when reading a Transaction."""

    # adds `id` from BaseDb


class TransactionModel(AsyncModel[TransactionOut]):
    """Database queries for Transaction objects."""

    def __init__(self, client: AsyncClient) -> None:
        super().__init__(client, "transaction", TransactionOut)
