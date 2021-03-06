"""Tests for common error handling across all routes."""

from typing import Tuple
from unittest import main, IsolatedAsyncioTestCase as TestCase
from uuid import UUID

# external test dependencies
from fastapi import Depends, FastAPI
from db_wrapper import AsyncClient as Client
from db_wrapper.model.base import NoResultFound
from pydantic import BaseModel  # pylint: disable=no-name-in-module
# internal test dependencies
from tests.helpers.application import FAKE_KEY, get_test_app, get_test_client
from tests.helpers.database import get_test_db

from src.security import create_auth_dep


class TestErrorCodes(TestCase):
    """Testing HTTP Status Codes returned."""

    async def test_request_bad_content_type_returns_415(self) -> None:
        """Responds 415 to POST requests with incorrect Content-Type."""
        async with get_test_client(
            get_test_app([('post', '/', lambda: 'a response')])
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
                get_test_app([('post', '/fake_route', test_handler)])
        ) as clients:
            client, _ = clients

            response = await client.post(
                '/fake_route',
                json={'data': "isn't a transaction"})

        self.assertEqual(422, response.status_code)

    async def test_no_result_in_database(self) -> None:
        """Responds 404 when no result is found for DB query."""
        async def raise_no_result() -> None:
            raise NoResultFound()

        async with get_test_client(
                get_test_app([('get', '/fake_route', raise_no_result)])
        ) as clients:
            client, _ = clients
            response = await client.get('/fake_route')

        self.assertEqual(404, response.status_code)

    async def test_unauthenticated_request_to_protected_route(self) -> None:
        """Responds 401 when unauthenticated request is received."""
        async def get_protected_test_app() -> Tuple[FastAPI, Client]:
            test_app, test_db = (await get_test_app([])())

            @test_app.get('/fake_route')
            async def protected_route(user_id: UUID = Depends(
                    create_auth_dep(test_db, FAKE_KEY))) -> UUID:
                return user_id

            return test_app, test_db

        async with get_test_client(
                get_protected_test_app
        ) as clients:
            client, _ = clients
            response = await client.get('/fake_route')

        self.assertEqual(401, response.status_code)


if __name__ == "__main__":
    main()
