"""Test helper methods."""

from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple, TypeVar
from uuid import UUID
from unittest.mock import Mock

from db_wrapper.model import (
    sql,
    ModelData,
    AsyncModel,
)

from manage import sync, Config as ManageConfig

from src.database import ConnectionParameters, Client


#
# MOCK FACTORIES
#

def mock_client() -> Client:
    """Return a mocked client instance."""
    conn_params = ConnectionParameters('a', 0, 'a', 'a', 'a')

    return Mock(Client(conn_params))


AnyModelData = TypeVar('AnyModelData', bound=ModelData)
AnyAsyncModel = TypeVar('AnyAsyncModel', bound=AsyncModel[Any])


def mock_model(model: AnyAsyncModel) -> AnyAsyncModel:
    """Return a mocked model instance."""
    create = Mock(spec=model.create)
    read = Mock(spec=model.read)
    update = Mock(spec=model.update)
    delete = Mock(spec=model.delete)

    model = Mock(spec=model)
    model.create = create
    model.read = read
    model.update = update
    model.delete = delete

    return model

#
# TEST DB MANAGEMENT
#


async def clear_test_db(
    db_client: Client,
    config: ConnectionParameters
) -> None:
    """Drop all public in given database client."""
    query = sql.SQL("""
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        GRANT ALL ON SCHEMA public TO {user};
        GRANT ALL ON SCHEMA public TO public;
        COMMENT ON SCHEMA public IS 'standard public schema';
    """).format(user=sql.Identifier(config.user))

    await db_client.connect()
    await db_client.execute(query)
    await db_client.disconnect()


async def get_test_db() -> Tuple[ConnectionParameters, Client]:
    """Create database client & return it."""
    # test database connection data
    user = 'test'
    password = 'pass'
    host = 'localhost'
    port = 9432
    database = 'test'

    # create app database client
    test_db_params = ConnectionParameters(host, port, user, password, database)
    test_client = Client(test_db_params)

    # drop any existing test tables
    await clear_test_db(test_client, test_db_params)

    # rebuild database from app model schema
    config = ManageConfig(user, password, host, port, database)
    sync(['silent', 'noprompt'], config)

    return test_db_params, test_client


#
# INSERT DATA
#


async def setup_user(database: Client, handle: str = "user") -> UUID:
    """Set up database with 2 users for testing."""
    query = sql.SQL("""
        INSERT INTO
            hoops_user(handle, full_name, preferred_name, password)
        VALUES
            ({handle}, 'A Full Name', 'Nickname', '@ new p4s5w0rd')
        RETURNING id;
    """).format(
        handle=sql.Literal(handle)
    )

    await database.connect()
    result: List[Dict[str, UUID]] = await database.execute_and_return(query)
    await database.disconnect()

    return result[0]["id"]


async def setup_account(
    database: Client,
    user_id: Optional[UUID] = None
) -> UUID:
    """Set up database with 1 account for given user for testing."""
    if not user_id:
        user_id = await setup_user(database)

    query = sql.SQL("""
        INSERT INTO account(user_id, name)
        VALUES ({user_id}, {name})
        RETURNING id;
    """).format(
        user_id=sql.Literal(user_id),
        name=sql.Literal("an account"))

    await database.connect()
    result: List[Dict[str, UUID]] = await database.execute_and_return(query)
    await database.disconnect()

    return result[0]["id"]


async def setup_transactions(
    database: Client,
    amounts: List[Decimal],
    account_id: Optional[UUID] = None,
) -> None:
    """Set up database with transactions of given amounts."""
    if not account_id:
        account_id = await setup_account(database)

    def build_transaction(amount: Decimal) -> sql.Composed:
        return sql.SQL("""
            ({amount},
             'payee',
             'description',
             '2019-12-10T08:12-05:00',
             {account_id})
        """).format(
            amount=sql.Literal(amount),
            account_id=sql.Literal(account_id))

    query = sql.SQL("""
        INSERT INTO
            transaction(amount, payee, description, timestamp, account_id)
        VALUES {amounts};
    """).format(
        amounts=sql.SQL(",").join(
            [build_transaction(amount) for amount in amounts]))

    await database.connect()
    await database.execute(query)
    await database.disconnect()


async def setup_envelope(
    database: Client,
    user_id: UUID,
    account_id: UUID,
    transaction_amounts: List[Decimal] = [Decimal(10)],
    name: Optional[str] = "envelope",
    funds: Optional[Decimal] = Decimal(0),
) -> UUID:
    """Create Envelope, optionally with given name & funds."""
    await setup_transactions(database, transaction_amounts, account_id)

    add_envelopes_query = sql.SQL("""
        INSERT INTO envelope
            (name, total_funds, user_id)
        VALUES
            ({name}, {funds}, {user_id})
        RETURNING
            id;
    """).format(
        name=sql.Literal(name),
        funds=sql.Literal(funds),
        user_id=sql.Literal(user_id))

    await database.connect()
    query_result = \
        await database.execute_and_return(add_envelopes_query)
    await database.disconnect()

    result: UUID = query_result[0]["id"]

    return result
