"""DB Model for User objects."""

from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from db_wrapper.client import AsyncClient
from db_wrapper.model import (
    sql,
    ModelData,
    AsyncModel,
    AsyncCreate,
    AsyncRead,
    AsyncUpdate,
    RealDictRow,
)
from db_wrapper.model.base import NoResultFound
from pydantic import (  # pylint: disable=no-name-in-module
    BaseModel,
)


class UserBase(BaseModel):  # pylint: disable=R0903
    """Common fields to all User objects."""

    handle: str
    full_name: str
    preferred_name: str


class UserIn(UserBase):  # pylint: disable=R0903
    """Fields required to create a new User."""

    password: str


class UserChanges(BaseModel):  # pylint: disable=R0903
    """Fields used when updating a User, all are optional."""

    handle: Optional[str]
    full_name: Optional[str]
    preferred_name: Optional[str]


class UserOut(UserBase, ModelData):  # pylint: disable=R0903
    """Fields returned by queries on User Model."""


class UserDb(UserIn, ModelData):  # pylint: disable=R0903
    """All fields on User in database records."""


class UserCreator(AsyncCreate[UserOut]):  # pylint: disable=R0903
    """User creation methods."""

    async def one(self, _: UserOut) -> UserOut:
        """Un-implemented to force use of create.new method."""
        raise NotImplementedError()

    async def new(self, user: UserIn) -> UserOut:
        """Replace default create.one to change input types."""
        query = sql.SQL("""
            INSERT INTO {table}(
                handle,
                password,
                full_name,
                preferred_name
            )
            VALUES (
                {handle},
                crypt({password}, gen_salt('bf')),
                {full_name},
                {preferred_name}
            )
            RETURNING id, handle, full_name, preferred_name, password;
        """).format(
            table=self._table,
            handle=sql.Literal(user.handle),
            password=sql.Literal(user.password),
            full_name=sql.Literal(user.full_name),
            preferred_name=sql.Literal(user.preferred_name))

        query_result: List[RealDictRow] = \
            await self._client.execute_and_return(query)
        print(query_result)
        result: UserOut = self._return_constructor(**query_result[0])

        return result


class UserReader(AsyncRead[UserOut]):
    """Extended read methods for UserModel."""

    async def authenticate(self, handle: str, password: str) -> UserOut:
        """Authorize user via given username & password, return User."""
        query = sql.SQL("""
            SELECT
                id, handle, full_name, preferred_name
            FROM
                {table}
            WHERE
                handle = {handle} AND
                password = crypt({password}, password);
        """).format(
            table=self._table,
            handle=sql.Literal(handle),
            password=sql.Literal(password))

        query_result = await self._client.execute_and_return(query)

        try:
            return UserOut(**query_result[0])
        except IndexError as err:
            raise NoResultFound from err


class UserUpdater(AsyncUpdate[UserOut]):
    """Extended Updater for UserModel."""

    async def one_by_id(self, _: str, __: Dict[str, Any]) -> UserOut:
        """Un-implemented to force use of update.changes method."""
        raise NotImplementedError()

    async def changes(self, user_id: UUID, changes: UserChanges) -> UserOut:
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

        query = sql.SQL(
            'UPDATE {table} '
            'SET {changes} '
            'WHERE id = {id_value} '
            'RETURNING *;'
        ).format(
            table=self._table,
            changes=compose_changes(changes.dict()),
            id_value=sql.Literal(str(user_id)),
        )
        query_result = await self._client.execute_and_return(query)

        try:
            return UserOut(**query_result[0])
        except IndexError as err:
            raise NoResultFound from err

    async def password(self, user_id: UUID, new_password: str) -> UserOut:
        """Update the given user's password."""
        query = sql.SQL("""
            UPDATE {table}
            SET password = crypt({password}, gen_salt('bf'))
            WHERE id = {user_id}
            RETURNING id, handle, full_name, preferred_name;
        """).format(
            table=self._table,
            password=sql.Literal(new_password),
            user_id=sql.Literal(str(user_id))
        )
        query_result = await self._client.execute_and_return(query)

        try:
            return UserOut(**query_result[0])
        except IndexError as err:
            raise NoResultFound from err


class UserModel(AsyncModel[UserOut]):  # pylint: disable=R0903
    """Database queries for User objects."""

    create: UserCreator
    read: UserReader
    update: UserUpdater

    def __init__(self, client: AsyncClient) -> None:
        """Replace built-in Creator & Reader with extended versions."""
        super().__init__(client, "hoops_user", UserOut)
        self.create = UserCreator(client, self.table, UserOut)
        self.read = UserReader(client, self.table, UserOut)
        self.update = UserUpdater(client, self.table, UserOut)
