"""Test factories for models.transaction."""

from uuid import uuid1

from src.models import transaction


class TransactionBase:
    @staticmethod
    def create() -> transaction.TransactionBase:
        return transaction.TransactionBase(
            amount="1.00",
            description="a description",
            payee="a payee",
            timestamp="2019-12-10T08:12-05:00"
        )


class TransactionDB:
    @staticmethod
    def create() -> transaction.TransactionDB:
        return transaction.TransactionDB(**{
            **TransactionBase.create().dict(),
            "id": uuid1()
        })
