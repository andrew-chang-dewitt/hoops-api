from datetime import datetime
from typing import Any, Dict
from uuid import uuid1

from hoops import models


class TransactionData:
    """TransactionData object factory methods."""

    @staticmethod
    def create() -> models.TransactionData:
        return models.TransactionData(**{
            "id": uuid1(),
            "amount": 1.0,
            "description": "a description",
            "payee": "a payee",
            "timestamp": datetime.fromisoformat("0001-01-01T00:00:00")
        })

    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        return cls.create().dict()
