"""Tests for /envelope routes."""

from unittest import main, IsolatedAsyncioTestCase as TestCase
from uuid import UUID

from db_wrapper.model import sql

# internal test dependencies
from tests.helpers.application import (
    get_test_client,
    get_token_header,
)
from tests.helpers.database import (
    setup_user,
    setup_account,
    setup_transactions,
)
from src.database import Client

BASE_URL = "/envelope"


class TestRoutePostRoot(TestCase):
    """Testing POST /envelope."""

    # FIXME: nothing below has been updated to current tests yet

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            user_id = await setup_user(database)

            new_envelope = {
                "name": "envelope",
            }

            response = await client.post(
                BASE_URL,
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"},
                json=new_envelope)

            with self.subTest(
                    msg="Responds with a status code of 201."):
                self.assertEqual(201, response.status_code)


if __name__ == "__main__":
    main()
