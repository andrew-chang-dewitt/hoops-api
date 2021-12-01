"""Routes under `/envelope`."""

from typing import List
from uuid import uuid1, UUID

from fastapi import Depends
from fastapi.routing import APIRouter

from src.config import Config
from src.database import Client
from src.models import (
    EnvelopeChanges,
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

    @envelope.get(
        "",
        response_model=List[EnvelopeOut],
        summary="Get all Envelopes for current user."
    )
    async def get_root(
        user_id: UUID = Depends(auth_user)
    ) -> List[EnvelopeOut]:
        return await model.read.many_by_user(user_id)

    @envelope.get(
        "/{envelope_id}",
        response_model=EnvelopeOut,
        summary="Get requested Envelope for current user."
    )
    async def get_id(
        envelope_id: UUID,
        user_id: UUID = Depends(auth_user)
    ) -> EnvelopeOut:
        return await model.read.one(envelope_id, user_id)

    @envelope.put(
        "/{envelope_id}",
        response_model=EnvelopeOut,
        summary="Update the given Envelope."
    )
    async def put_id(
        envelope_id: UUID,
        changes: EnvelopeChanges,
        user_id: UUID = Depends(auth_user),
    ) -> EnvelopeOut:
        return await model.update.changes(envelope_id, user_id, changes)

    return envelope
