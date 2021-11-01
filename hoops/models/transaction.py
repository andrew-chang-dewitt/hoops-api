"""A Model for Transaction data types."""

import datetime
from decimal import Decimal
from typing import List, Optional

from db_wrapper.client import SyncClient
from db_wrapper.model import (
    ModelData,
    RealDictRow,
    SyncModel,
    SyncRead,
    sql,
)


class TransactionData(ModelData):
    """An example Item."""

    # Essentially a dataclass, has no methods
    # pylint: disable=too-few-public-methods

    amount: Decimal
    description: str
    payee: str
    timestamp: datetime.datetime


class TransactionReader(SyncRead[TransactionData]):
    """Additional read methods."""

    def many(self, limit: Optional[int]) -> List[TransactionData]:
        """Return many transaction records."""
        query = sql.SQL(
            'SELECT * '
            'FROM {table} '
            'ORDER BY timestamp '
            'LIMIT {limit}'
        ).format(
            table=self._table,
            limit=sql.Literal(limit),
        )

        query_result: List[RealDictRow] = \
            self._client.execute_and_return(query)
        result = [self._return_constructor(**row)
                  for row in query_result]

        return result


class Transaction(SyncModel[TransactionData]):
    """Build an Transaction Model instance."""

    read: TransactionReader

    def __init__(self, client: SyncClient) -> None:
        table = 'transaction'

        super().__init__(client, table, TransactionData)
        self.read = TransactionReader(client, self.table, TransactionData)
