"""DB Model for Transaction objects."""

from datetime import datetime
from typing import List
from uuid import UUID

from db_wrapper.client import AsyncClient
from db_wrapper.model import (
    sql,
    AsyncModel,
    AsyncCreate,
    AsyncRead,
)
from db_wrapper.model.base import NoResultFound
from pydantic import ConstrainedDecimal  # pylint: disable=E0611

from src.models.base import Base, BaseDb


class Amount(ConstrainedDecimal):
    """A Decimal, constrained to 2 decimal places."""

    # pylint: disable=too-few-public-methods

    decimal_places = 2


class TransactionBase(Base):
    """Base Transaction fields."""

    amount: Amount
    description: str
    payee: str
    timestamp: datetime
    account_id: UUID


class TransactionIn(TransactionBase):
    """Fields used when creating a new Transaction."""

    # simply a copy of TransactionBase for now


class TransactionOut(TransactionBase, BaseDb):
    """Fields used when reading a Transaction."""

    # adds `id` from BaseDb


class TransactionCreator(AsyncCreate[TransactionOut]):
    """Extend default create methods."""

    async def new(self, new_tran: TransactionIn) -> TransactionOut:
        """Create & return new Transaction."""
        columns: List[sql.Identifier] = []
        values: List[sql.Literal] = []

        for column, value in new_tran.dict().items():
            values.append(sql.Literal(value))

            columns.append(sql.Identifier(column))

        query = sql.SQL(
            'INSERT INTO {table} ({columns}) '
            'VALUES ({values}) '
            'RETURNING *;'
        ).format(
            table=self._table,
            columns=sql.SQL(',').join(columns),
            values=sql.SQL(',').join(values),
        )

        query_result = await self._client.execute_and_return(query)

        return TransactionOut(**query_result[0])


class TransactionReader(AsyncRead[TransactionOut]):
    """Extended read methods."""

    async def many_by_user(self, user_id: UUID) -> List[TransactionOut]:
        """Get list of Transactions for User."""
        query = sql.SQL("""
            SELECT
                t.id as id,
                t.amount as amount,
                t.payee as payee,
                t.description as description,
                t.timestamp as timestamp,
                t.account_id as account_id
            FROM
                {table} as t
            INNER JOIN
                account as a
            ON
                a.id = t.account_id
            WHERE
                a.user_id = {user_id};
        """).format(
            table=self._table,
            user_id=sql.Literal(user_id)
        )

        query_result = await self._client.execute_and_return(query)

        return [TransactionOut(**tran) for tran in query_result]


class TransactionModel(AsyncModel[TransactionOut]):
    """Database queries for Transaction objects."""

    create: TransactionCreator
    read: TransactionReader

    def __init__(self, client: AsyncClient) -> None:
        """Override default CRUD methods & defer remaining to super."""
        super().__init__(client, "transaction", TransactionOut)
        self.create = TransactionCreator(client, self.table, TransactionOut)
        self.read = TransactionReader(client, self.table, TransactionOut)
