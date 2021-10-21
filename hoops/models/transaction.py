"""A Model for Transaction data types."""

import datetime

from db_wrapper.model import (
    ModelData,
    Model,
)


class TransactionData(ModelData):
    """An example Item."""

    amount: float
    description: str
    payee: str
    date: datetime.date


class Transaction(Model[TransactionData]):
    """Build an Transaction Model instance."""
