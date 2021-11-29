"""DB Model for Envelope objects."""

from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from db_wrapper.client import AsyncClient
from db_wrapper.model import (
    sql,
    AsyncCreate,
    AsyncRead,
    AsyncUpdate,
    AsyncModel,
)
from db_wrapper.model.base import ensure_exactly_one

from src.models.amount import Amount
from src.models.base import Base, BaseDb


class EnvelopeIn(Base):
    """Fields needed from user to create an Envelope."""

    name: str


class EnvelopeNew(EnvelopeIn):
    """Information needed to save a new envelope to the database."""

    user_id: UUID


class EnvelopeOut(EnvelopeNew, BaseDb):
    """Fields returned by Envelope queries."""

    total_funds: Amount


class EnvelopeChanges(Base):
    """Fields used when updating an Envelope, all are optional."""

    name: Optional[str]
    total_funds: Optional[Amount]


class EnvelopeCreator(AsyncCreate[EnvelopeOut]):
    """Extended create methods."""

    async def new(self, data: EnvelopeNew) -> EnvelopeOut:
        """Create a new Envelope."""
        query = sql.SQL("""
                INSERT INTO {table}(user_id, name, total_funds)
                VALUES ({user_id}, {name}, {total_funds})
                RETURNING *;
                """).format(
            table=self._table,
            user_id=sql.Literal(str(data.user_id)),
            name=sql.Literal(data.name),
            total_funds=sql.Literal(0))

        query_result = \
            await self._client.execute_and_return(query)

        return EnvelopeOut(**query_result[0])


class EnvelopeReader(AsyncRead[EnvelopeOut]):
    """Extended read methods."""

    async def one(
            self,
            envelope_id: UUID,
            user_id: UUID,
    ) -> EnvelopeOut:
        """Get a single envelope for given user & id."""
        query = sql.SQL("""
            SELECT * FROM {table}
            WHERE id = {envelope_id}
            AND user_id = {user_id};
        """).format(
            table=self._table,
            envelope_id=sql.Literal(str(envelope_id)),
            user_id=sql.Literal(str(user_id)))
        query_result = await self._client.execute_and_return(query)

        ensure_exactly_one(query_result)

        return EnvelopeOut(**query_result[0])

    async def many_by_user(
        self,
        user_id: UUID,
    ) -> List[EnvelopeOut]:
        """Get list of envelopes for user."""
        query = sql.SQL("""
            SELECT * FROM {table}
            WHERE user_id = {user_id};
        """).format(
            table=self._table,
            user_id=sql.Literal(str(user_id)))
        query_result = await self._client.execute_and_return(query)

        return [EnvelopeOut(**envelope) for envelope in query_result]


class EnvelopeModel(AsyncModel[EnvelopeOut]):
    """Envelope database methods."""

    create: EnvelopeCreator
    read: EnvelopeReader
    # update: EnvelopeUpdater

    def __init__(self, client: AsyncClient) -> None:
        """Create Envelope Model."""
        super().__init__(client, "envelope", EnvelopeOut)
        self.create = EnvelopeCreator(client, self.table, EnvelopeOut)
        self.read = EnvelopeReader(client, self.table, EnvelopeOut)
        # self.update = EnvelopeUpdater(client, self.table, EnvelopeOut)
