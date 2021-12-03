"""Routes under `/envelope`."""

from typing import List, Optional
from uuid import UUID

from fastapi import status, Depends, Query
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from src.config import Config
from src.database import Client
from src.models import (
    BalanceModel,
    EnvelopeChanges,
    EnvelopeIn,
    EnvelopeNew,
    EnvelopeOut,
    EnvelopeModel as Model
)
from src.models.amount import Amount
from src.security import create_auth_dep


def create_envelope(config: Config, database: Client) -> APIRouter:
    """Create a envelope router & model with access to the given database."""
    # setup db & Envelope model
    model = Model(database)
    balance_model = BalanceModel(database)
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
        summary="Update the given Envelope.",
    )
    async def put_id(
        envelope_id: UUID,
        changes: EnvelopeChanges,
        user_id: UUID = Depends(auth_user),
    ) -> EnvelopeOut:
        return await model.update.changes(envelope_id, user_id, changes)

    default_source = Query(
        None,
        description="Where take funds from; default: Available Balance.")

    @envelope.put(
        "/{envelope_id}/funds/{amount}",
        response_model=EnvelopeOut,
        summary="Add given funds to Envelope.",
    )
    async def put_funds(
        envelope_id: UUID,
        amount: Amount,
        source: Optional[UUID] = default_source,
        user_id: UUID = Depends(auth_user),
    ) -> EnvelopeOut:
        # get source balance
        if source is None:
            source_balance = \
                await balance_model.read.all_minus_allocated(user_id)

        else:
            source_balance = \
                await balance_model.read.one_by_collection(source, user_id)

        # calculate new source balance & check if enough funds in source
        new_source_amount = source_balance.amount - amount

        if new_source_amount < 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Not enough funds available in source.")

        # if source is envelope, update source balance
        if source is not None:
            new_source = EnvelopeChanges(total_funds=new_source_amount)
            await model.update.changes(source, user_id, new_source)

        # get current envelope data & calculate new funds value
        existing = await model.read.one(envelope_id, user_id)
        new_funds_amount = existing.total_funds + amount

        # create changes object & save to db, returning result
        funds_added = EnvelopeChanges(total_funds=new_funds_amount)
        return await model.update.changes(envelope_id, user_id, funds_added)

    return envelope
