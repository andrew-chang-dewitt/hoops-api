"""DB Model for Balance objects."""

from typing import Literal, Optional, Union
from uuid import UUID

from db_wrapper.client import AsyncClient
from db_wrapper.model import sql

from src.models.amount import Amount
from src.models.base import Base


class Balance(Base):
    """Balance information."""

    amount: Amount
    collection: Optional[str]  # the name of the list of Transactions
    # this Balance is associated with
    collection_id: Optional[UUID]
    collection_type: Optional[Union[Literal["account"], Literal["envelope"]]]
    user_id: UUID


class BalanceReader:
    """Database read queries for Balance objects."""

    def __init__(self, client: AsyncClient, table: sql.Literal) -> None:
        """Create Balance reader."""
        self._client = client
        self._table = table

    async def all_accounts_by_user(self, user_id: UUID) -> Balance:
        """Get the sum total Balance of all accounts for given User."""
        query = sql.SQL("""
            SELECT sum(amount) as amount, user_id
            FROM {table}
            WHERE user_id = {user_id}
            AND collection_type = 'account'
            GROUP BY user_id;
        """).format(
            table=self._table,
            user_id=sql.Literal(user_id))
        query_result = await self._client.execute_and_return(query)

        return Balance(**query_result[0])

    async def one_by_collection(
            self, collection_id: UUID, user_id: UUID) -> Balance:
        """Get the Balance for the given collection."""
        query = sql.SQL("""
            SELECT *
            FROM {table}
            WHERE collection_id = {collection_id}
            AND user_id = {user_id};
        """).format(
            table=self._table,
            collection_id=sql.Literal(collection_id),
            user_id=sql.Literal(user_id))
        query_result = await self._client.execute_and_return(query)

        return Balance(**query_result[0])

    async def all_minus_allocated(self, user_id: UUID) -> Balance:
        """Get the User's Available Balance."""
        query = sql.SQL("""
            SELECT
                coalesce(
                    (
                        SELECT sum(amount)
                        FROM {table}
                        WHERE user_id = {user_id}
                        AND collection_type = 'account'
                    ),
                    0
                ) - coalesce(
                    (
                        SELECT sum(amount)
                        FROM {table}
                        WHERE user_id = {user_id}
                        AND collection_type = 'envelope'
                    ),
                    0
                )
                 AS amount,
                user_id
            FROM
                {table}
            WHERE
                user_id = {user_id}
            GROUP BY
                user_id;
        """).format(
            table=self._table,
            user_id=sql.Literal(user_id))
        query_result = await self._client.execute_and_return(query)

        print(f"query result: {query_result}")

        return Balance(**query_result[0])


class BalanceModel:
    """Database queries for Balance objects."""

    client: AsyncClient
    table: sql.Identifier

    def __init__(self, client: AsyncClient) -> None:
        """Create Balance Model."""
        self.client = client
        self.table = sql.Identifier("balance")
        self.read = BalanceReader(client, self.table)
