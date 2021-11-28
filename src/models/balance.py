"""DB Model for Balance objects."""

from uuid import UUID

from db_wrapper.client import AsyncClient
from db_wrapper.model import (
    sql,
    AsyncRead,
    AsyncModel,
)

from src.models.amount import Amount
from src.models.base import Base


class Balance(Base):
    """Balance information."""

    amount: Amount
    collection: str  # the name of the list of Transactions
    # this Balance is associated with
    collection_id: UUID
    user_id: UUID


class BalanceReader:
    """Database read queries for Balance objects."""

    def __init__(self, client: AsyncClient, table: sql.Literal) -> None:
        self._client = client
        self._table = table

    async def one_by_account(
            self, account_id: UUID, user_id: UUID) -> Balance:
        """Get the Balance for the given account."""

        query = sql.SQL("""
            SELECT *
            FROM {table}
            WHERE collection_id = {account_id}
            AND user_id = {user_id};
        """).format(
            table=self._table,
            account_id=sql.Literal(account_id),
            user_id=sql.Literal(user_id))
        query_result = await self._client.execute_and_return(query)

        return Balance(**query_result[0])


class BalanceModel:
    """Database queries for Balance objects."""

    client: AsyncClient
    table: sql.Identifier

    def __init__(self, client: AsyncClient) -> None:
        self.client = client
        self.table = sql.Identifier("balance")
        self.read = BalanceReader(client, self.table)
