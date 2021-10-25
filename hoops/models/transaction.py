"""A Model for Transaction data types."""

import datetime

from db_wrapper.client import SyncClient
from db_wrapper.model import (
    ModelData,
    SyncModel,
)


class TransactionData(ModelData):
    """An example Item."""

    amount: float
    description: str
    payee: str
    date: datetime.date


class Transaction(SyncModel[TransactionData]):
    """Build an Transaction Model instance."""

    def __init__(self, client: SyncClient) -> None:
        super().__init__(client, 'transaction')
