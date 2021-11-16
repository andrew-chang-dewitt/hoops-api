"""Test helper methods."""

from typing import Any, Tuple, TypeVar
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
    sync(['noprompt'], config)

    return test_db_params, test_client
