from typing import Any, Dict
from uuid import uuid1

from src.models import EnvelopeOut as SrcEnvelopeOut


class EnvelopeOut:
    """Create test Envelope objects."""

    @staticmethod
    def create(**kwargs: Any) -> SrcEnvelopeOut:
        """Create EnvelopeOut."""
        return SrcEnvelopeOut(**{
            "id": uuid1(),
            "user_id": uuid1(),
            "name": "envelope",
            "total_funds": 0,
            **kwargs,
        })
