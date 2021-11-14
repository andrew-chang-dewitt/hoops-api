"""A Model for Transaction data types."""

import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import (  # pylint: disable=no-name-in-module
    BaseModel,
    ConstrainedDecimal
)

from db_wrapper.client import AsyncClient
from db_wrapper.model import (
    ModelData,
    RealDictRow,
    AsyncModel,
    AsyncCreate,
    AsyncRead,
    sql,
)


class Amount(ConstrainedDecimal):
    """A Decimal, constrained to 2 decimal places."""

    # pylint: disable=too-few-public-methods

    decimal_places = 2


class TransactionBase(BaseModel):
    """Core Transaction data fields."""

    # Essentially a dataclass, has no methods
    # pylint: disable=too-few-public-methods

    amount: Amount
    description: str
    payee: str
    timestamp: datetime.datetime


class TransactionDB(ModelData, TransactionBase):  # pylint: disable=R0903
    """Transactions in database have an ID."""


class TransactionCreator(AsyncCreate[TransactionDB]):
    """Additional/updated create methods."""

    # pylint: disable=too-few-public-methods

    async def one(self, transaction: TransactionBase) -> TransactionDB:
        """Save a new transaction to the database."""
        columns: List[sql.Identifier] = []
        values: List[sql.Literal] = []

        for column, value in transaction.dict().items():
            values.append(sql.Literal(value))

            columns.append(sql.Identifier(column))

        query = sql.SQL("""
            INSERT INTO {table} ({columns}) 
            VALUES ({values}) 
            RETURNING *;
        """).format(
            table=self._table,
            columns=sql.SQL(',').join(columns),
            values=sql.SQL(',').join(values),
        )

        query_result: List[RealDictRow] = \
            await self._client.execute_and_return(query)
        result: TransactionDB = self._return_constructor(**query_result[0])

        return result


class TransactionReader(AsyncRead[TransactionDB]):
    """Additional read methods."""

    async def many(
        self,
        limit: Optional[int],
        page: Optional[int]
    ) -> List[TransactionDB]:
        """Return many transaction records."""
        # default to 50 records
        actual_limit = limit if limit is not None else 50
        # default to first 0th page
        actual_page = page if page is not None else 0
        # offset is n times limit
        # if limit = 50: (0, 0), (1, 50), ... (n+1, 50*n)
        offset = actual_page * actual_limit

        query = sql.SQL(
            'SELECT * '
            'FROM {table} '
            'ORDER BY timestamp DESC '
            'LIMIT {limit} OFFSET {offset};'
        ).format(
            table=self._table,
            limit=sql.Literal(actual_limit),
            offset=sql.Literal(offset),
        )

        query_result: List[RealDictRow] = \
            await self._client.execute_and_return(query)
        result = [self._return_constructor(**row)
                  for row in query_result]

        return result


class TransactionModel(AsyncModel[TransactionDB]):
    """Database queries for Transaction objects."""

    create: TransactionCreator
    read: TransactionReader

    def __init__(self, client: AsyncClient) -> None:
        table = 'transaction'

        super().__init__(client, table, TransactionDB)
        self.create = TransactionCreator(client, self.table, TransactionDB)
        self.read = TransactionReader(client, self.table, TransactionDB)
