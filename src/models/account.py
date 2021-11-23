"""DB Model for Account objects."""

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
from db_wrapper.model.base import NoResultFound

from src.models.base import Base, BaseDb


class AccountIn(Base):
    """Fields needed from user to create an Account."""

    name: str


class AccountChanges(Base):
    """Fields used when updating an Account, all are optional."""

    name: Optional[str]
    closed: Optional[bool]


class AccountNew(AccountIn):
    """Information needed to save a new account to the database."""

    user_id: UUID


class AccountOut(AccountNew, BaseDb):
    """Fields returned by Account queries."""

    closed: bool


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

    async def many_by_user(
        self,
        user_id: UUID,
        **kwargs: Any
    ) -> List[AccountOut]:
        """Get list of accounts for user."""
        def build_one_filter(column: str, value: Any) -> sql.Composed:
            return sql.SQL(
                "AND {column} = {value}"
            ).format(
                column=sql.Identifier(column),
                value=sql.Literal(value))

        def build_filters(filters: AccountChanges) -> sql.Composed:
            filter_queries: List[sql.Composed] = []

            for key, value in filters.dict().items():
                if value is not None:
                    filter_queries.append(build_one_filter(key, value))

            return sql.SQL(" ").join(filter_queries)

        filter_values = AccountChanges(**{
            # default to filtering by accounts not marked as closed
            "closed": False,
            # and override default if it's present in kwargs
            **kwargs,
        })

        query = sql.SQL("""
            SELECT * FROM {table}
            WHERE user_id = {user_id}
            {filters};
        """).format(
            table=self._table,
            user_id=sql.Literal(str(user_id)),
            filters=build_filters(filter_values))
        query_result = \
            await self._client.execute_and_return(query)

        return [AccountOut(**account) for account in query_result]


class AccountUpdater(AsyncUpdate[AccountOut]):
    """Extended update methods."""

    async def one_by_id(self, _: str, __: Dict[str, Any]) -> AccountOut:
        """Un-implemented to force use of update.changes method."""
        raise NotImplementedError()

    async def changes(
        self,
        account_id: UUID,
        user_id: UUID,
        changes: AccountChanges
    ) -> AccountOut:
        """Update only the given fields for the given user."""
        def compose_one_change(change: Tuple[str, Any]) -> sql.Composed:
            key = change[0]
            value = change[1]

            return sql.SQL("{key} = {value}").format(
                key=sql.Identifier(key), value=sql.Literal(value))

        def compose_changes(changes: Dict[str, Any]) -> sql.Composed:
            return sql.SQL(',').join(
                [compose_one_change(change)
                 for change in changes.items()
                 if change[1]])

        query = sql.SQL("""
            UPDATE {table}
            SET {changes}
            WHERE id = {account_id}
            AND user_id = {user_id}
            RETURNING *;
        """).format(
            table=self._table,
            changes=compose_changes(changes.dict()),
            account_id=sql.Literal(account_id),
            user_id=sql.Literal(user_id),
        )
        query_result = await self._client.execute_and_return(query)

        try:
            return AccountOut(**query_result[0])
        except IndexError as err:
            raise NoResultFound from err


class AccountModel(AsyncModel[AccountOut]):
    """Account ORM."""

    create: AccountCreator
    read: AccountReader
    update: AccountUpdater

    def __init__(self, client: AsyncClient) -> None:
        """Create Account Model."""
        super().__init__(client, "account", AccountOut)
        self.create = AccountCreator(client, self.table, AccountOut)
        self.read = AccountReader(client, self.table, AccountOut)
        self.update = AccountUpdater(client, self.table, AccountOut)
