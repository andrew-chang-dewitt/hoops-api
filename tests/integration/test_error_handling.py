"""Tests for common error handling across all routes."""

from contextlib import asynccontextmanager
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Callable,
    Optional,
    Tuple,
)
from unittest import main, IsolatedAsyncioTestCase as TestCase

# external test dependencies
from asgi_lifespan import LifespanManager
from db_wrapper.model import sql
from db_wrapper.model.base import NoResultFound
from fastapi import FastAPI
from httpx import AsyncClient
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from manage import sync, Config as ManageConfig

# module under test
from src import create_app
# internal module dependencies
from src.config import Config as AppConfig
from src.database import Client, ConnectionParameters


BASE_URL = "http://localhost:8000"


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


async def get_test_app(
    database: Optional[ConnectionParameters] = None
) -> Tuple[FastAPI, Client]:
    """Create an application instance configured for testing."""
    if database is None:
        db_config, db_client = await get_test_db()

    test_config = AppConfig(
        database=db_config)
    return create_app(test_config), db_client


@asynccontextmanager
async def get_test_client(
    getter: Callable[..., Awaitable[Tuple[FastAPI, Client]]] = get_test_app
) -> AsyncGenerator[
        Tuple[AsyncClient, Client], None]:
    """Create test client for application with lifecycle events."""
    app, database = await getter()

    async with AsyncClient(
        app=app, base_url=BASE_URL
    ) as test_client, LifespanManager(app):
        yield test_client, database


AppGetter = Tuple[FastAPI, Client]


class TestErrorCodes(TestCase):
    """Testing HTTP Status Codes returned."""

    @staticmethod
    def app_getter(
        route: str,
        handler: Callable[..., Any]
    ) -> Callable[[], Awaitable[AppGetter]]:
        async def getter() -> Tuple[FastAPI, Client]:
            db_config, db_client = await get_test_db()

            test_config = AppConfig(
                database=db_config)
            test_app = create_app(test_config)
            # Add example route to show that this applies to all routes
            # on the application
            test_app.post(route)(handler)

            return test_app, db_client
        return getter

    async def test_request_bad_content_type_returns_415(self) -> None:
        """Responds 415 to POST requests with incorrect Content-Type."""
        async with get_test_client(
            self.app_getter('/', lambda: 'a response')
        ) as clients:
            client, _ = clients

            response = await client.post(
                '/',
                headers={'content-type': 'text/plain'},
                content='invalid data')

        self.assertEqual(415, response.status_code)

    async def test_request_isnt_transaction(self) -> None:
        """
        Responds 422 POST requests sending json that isn't the expected type.
        """
        class BodyType(BaseModel):
            field: int

        def test_handler(body_arg: BodyType) -> BodyType:
            return body_arg

        async with get_test_client(
                self.app_getter('/', test_handler)
        ) as clients:
            client, _ = clients

            response = await client.post(
                '/',
                json={'data': "isn't a transaction"})

        self.assertEqual(422, response.status_code)

    async def test_no_result_in_database(self) -> None:
        """Responds 404 when no result is found for DB query."""
        async def raise_no_result() -> None:
            raise NoResultFound()

        async with get_test_client(
                self.app_getter('/', raise_no_result)
        ) as clients:
            client, _ = clients
            response = await client.post('/', json={})

        self.assertEqual(404, response.status_code)


if __name__ == "__main__":
    main()
