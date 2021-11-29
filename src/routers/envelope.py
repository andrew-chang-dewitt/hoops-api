"""Routes under `/envelope`."""

from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter

from src.config import Config
from src.database import Client
from src.models import (
    EnvelopeIn,
    EnvelopeNew,
    EnvelopeOut,
    EnvelopeModel as Model
)
from src.security import create_auth_dep


def create_envelope(config: Config, database: Client) -> APIRouter:
    """Create a envelope router & model with access to the given database."""
    # setup db & Envelope model
    model = Model(database)
    # setup User auth dependency
    auth_user = create_auth_dep(database, config.jwt_key)

    # setup router
    envelope = APIRouter(prefix="/envelope", tags=["Envelope"])

    @envelope.post(
        "",
        status_code=201,
        response_model=EnvelopeOut,
        summary="Create new Envelope."
    )
    async def post_root(
        envelope: EnvelopeIn,
        user_id: UUID = Depends(auth_user)
    ) -> EnvelopeOut:
        return await model.create.new(
            EnvelopeNew(**envelope.dict(), user_id=user_id))

    return envelope
