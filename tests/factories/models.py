from datetime import datetime
from decimal import Decimal
import json
from typing import Any, Dict
from uuid import uuid1

from hoops import models
from hoops.app import ISODateJSONEncoder


class TransactionData:
    """TransactionData object factory methods."""

    @staticmethod
    def _schema() -> Dict[str, Any]:
        return {
            "id": uuid1(),
            "amount": Decimal("1.00"),
            "description": "a description",
            "payee": "a payee",
            "timestamp": datetime.fromisoformat("2019-12-10T08:12-05:00")
        }

    @classmethod
    def create(cls) -> models.TransactionData:
        return models.TransactionData(**cls._schema())

    @classmethod
    def create_with_data(cls, data: Dict[str, Any]) -> models.TransactionData:
        return models.TransactionData(**{
            **cls._schema(),
            **data,
        })

    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        return cls.create().dict()

    @classmethod
    def as_json(cls) -> str:
        return json.dumps(cls.as_dict(), cls=ISODateJSONEncoder)
