from typing import Any
from uuid import uuid1

from src.models import Balance as SrcBalance


class Balance:
    """Balance objects."""

    @staticmethod
    def create(**kwargs: Any) -> SrcBalance:
        """Create Balance object."""
        return SrcBalance(**{
            "amount": 0,
            "collection": None,
            "collection_id": None,
            "collection_type": None,
            "user_id": uuid1(),
            **kwargs,
        })
