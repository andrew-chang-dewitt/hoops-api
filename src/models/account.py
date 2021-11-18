"""DB Model for Account objects."""

from typing import List
from uuid import UUID

from db_wrapper.client import AsyncClient
from db_wrapper.model import (
    sql,
    AsyncCreate,
    AsyncRead,
    AsyncModel,
    ModelData,
)
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class AccountIn(BaseModel):
    """Fields needed from user to create an Account."""

    name: str


class AccountNew(AccountIn):
    """Information needed to save a new account to the database."""

    user_id: UUID


class AccountOut(AccountNew, ModelData):
    """Fields returned by Account queries."""


class AccountCreator(AsyncCreate[AccountOut]):
    """Extended create methods."""

    async def new(self, data: AccountNew) -> AccountOut:
        """Create a new Account."""
        query = sql.SQL("""
                INSERT INTO {table}(user_id, name)
                VALUES ({user_id}, {name})
                RETURNING *;
                """).format(
            table=self._table,
            user_id=sql.Literal(str(data.user_id)),
            name=sql.Literal(data.name),
        )

        query_result = \
            await self._client.execute_and_return(query)

        return AccountOut(**query_result[0])


class AccountReader(AsyncRead[AccountOut]):
    """Extended read methods."""

    async def many_by_user(self, user_id: UUID) -> List[AccountOut]:
        """Get list of accounts for user."""
        query = sql.SQL("""
            SELECT * FROM {table}
            WHERE user_id = {user_id}
        """).format(
            table=self._table,
            user_id=sql.Literal(str(user_id)))
        query_result = \
            await self._client.execute_and_return(query)

        return [AccountOut(**account) for account in query_result]


class AccountModel(AsyncModel[AccountOut]):
    """Account ORM."""

    create: AccountCreator
    read: AccountReader

    def __init__(self, client: AsyncClient) -> None:
        super().__init__(client, "account", AccountOut)
        self.create = AccountCreator(client, self.table, AccountOut)
        self.read = AccountReader(client, self.table, AccountOut)
