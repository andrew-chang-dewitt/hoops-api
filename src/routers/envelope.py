"""Routes under `/envelope`."""

from typing import List, Optional, Union
from uuid import UUID

from fastapi import status, Depends, Query
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from src.config import Config
from src.database import Client
from src.lib import FundsHolder, move_funds
from src.models import (
    Balance,
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
        print(f"changes: {changes}")
        try:
            return await model.update.changes(envelope_id, user_id, changes)
        except Exception as exc:
            print(f"exc caught: {exc}")
            raise Exception from exc

    default_other = Query(
        None,
        description="Where take funds from; default: Available Balance.")

    @envelope.put(
        "/{envelope_id}/funds/{funds}",
        response_model=EnvelopeOut,
        summary="Add given funds to Envelope.",
    )
    async def put_funds(
        envelope_id: UUID,
        funds: Amount,
        other: Optional[UUID] = default_other,
        user_id: UUID = Depends(auth_user),
    ) -> EnvelopeOut:
        """
        Add funds to (or remove funds from, if given as a negative) envelope.

        Optionally, include source/target envelope for funds to be taken
        from/sent to. Defaults to Available Balance if not given.
        """
        envelope_bal = await balance_model.read.one_by_collection(envelope_id,
                                                                  user_id)
        other_bal = \
            await balance_model.read.one_by_collection(other, user_id) \
            if other \
            else await balance_model.read.all_minus_allocated(user_id)

        # get balance of source
        source_balance = envelope_bal if funds < 0 else other_bal

        # short circuit route with failure message if not enough funds
        # available to move
        if source_balance.amount - funds < 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Not enough funds available in source.")

        # subtract funds from other, if it is an envelope, & save
        if other:
            await model.update.sum_funds(0 - funds,
                                         other,
                                         user_id)

        # then add funds to this envelope, save, & return
        return await model.update.sum_funds(funds,
                                            envelope_id,
                                            user_id)

    return envelope
