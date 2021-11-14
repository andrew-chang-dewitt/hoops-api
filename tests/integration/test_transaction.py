"""Tests for routes @ `/transaction`."""

from contextlib import asynccontextmanager
from datetime import datetime
from decimal import Decimal
from typing import AsyncGenerator, Optional, Tuple
from unittest import main, IsolatedAsyncioTestCase as TestCase
from uuid import UUID

# external test dependencies
from db_wrapper.model import sql
from fastapi import FastAPI
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
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
async def get_test_client() -> AsyncGenerator[
        Tuple[AsyncClient, Client], None]:
    """Create test client for application with lifecycle events."""
    app, database = await get_test_app()

    async with AsyncClient(
        app=app, base_url=BASE_URL
    ) as test_client, LifespanManager(app):
        yield test_client, database


class TestRoutePostOne(TestCase):
    """Tests for `POST /transaction/one`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            response = await client.post(
                '/transaction/one',
                json={
                    "amount": "1.00",
                    "description": "a description",
                    "payee": "a payee",
                    "timestamp": "2019-12-10T08:12-05:00"})

        with self.subTest(
                msg="Responds with status code of 201 Created."):
            self.assertEqual(201, response.status_code)

        with self.subTest(
                msg="Responds with Content-Type: application/json Header."):
            self.assertEqual(response.headers.get(
                'content-type'), 'application/json')

        with self.subTest(
                msg="Responds with newly created Transaction."):
            body = response.json()

            with self.subTest():
                # UUID() will throw an error if body["id"] isn't an id
                self.assertTrue(UUID(body["id"]))
            with self.subTest():
                self.assertEqual(body['amount'], 1.0)
            with self.subTest():
                self.assertEqual(body['description'], "a description")
            with self.subTest():
                self.assertEqual(body['payee'], "a payee")
            with self.subTest():
                self.assertEqual(body['timestamp'],
                                 "2019-12-10T13:12:00+00:00")

        with self.subTest(
                msg="New transaction is in database."):
            body = response.json()
            new_id = UUID(body["id"])

            await database.connect()
            query_result = await database.execute_and_return(sql.SQL("""
                SELECT * FROM transaction
                WHERE id = {tran_id};
                """).format(tran_id=sql.Literal(new_id)))
            await database.disconnect()

            result = query_result[0]

            with self.subTest():
                self.assertEqual(result["id"], new_id)
            with self.subTest():
                self.assertEqual(result['amount'], Decimal("1.00"))
            with self.subTest():
                self.assertEqual(result['description'], "a description")
            with self.subTest():
                self.assertEqual(result['payee'], "a payee")
            with self.subTest():
                self.assertEqual(result['timestamp'],
                                 datetime.fromisoformat(
                                     "2019-12-10T13:12:00+00:00"))

    async def test_request_bad_content_type_returns_415(self) -> None:
        """Responds 415 to POST requests with incorrect Content-Type."""
        async with get_test_client() as clients:
            client, _ = clients

            response = await client.post(
                '/transaction/one',
                headers={'content-type': 'text/plain'},
                content='invalid data')

        self.assertEqual(415, response.status_code)

    async def test_request_isnt_transaction(self) -> None:
        """
        Responds 422 to POST requests sending json that isn't a Transaction.
        """
        async with get_test_client() as clients:
            client, _ = clients

            response = await client.post(
                '/transaction/one',
                json={'data': "isn't a transaction"})

        self.assertEqual(422, response.status_code)


if __name__ == "__main__":
    main()
