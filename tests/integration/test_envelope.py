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

            with self.subTest(
                    msg="Responds with newly created Envelope's data."):
                body = response.json()

                with self.subTest(msg="Saves the given name."):
                    self.assertEqual(body["name"], new_envelope["name"])
                with self.subTest(msg="Bound to current user in auth token."):
                    self.assertEqual(body["user_id"], str(user_id))
                with self.subTest(msg="Has a UUID identifier."):
                    self.assertTrue(UUID(body["id"]))
                with self.subTest(msg="Starts with zero funds."):
                    self.assertEqual(body["total_funds"], 0)

            with self.subTest(msg="Saves the Envelope to the database."):
                body = response.json()
                new_id = UUID(body["id"])

                await database.connect()
                query_result = await database.execute_and_return(sql.SQL("""
                    SELECT * FROM envelope
                    WHERE id = {new_id};
                """).format(new_id=sql.Literal(new_id)))
                await database.disconnect()

                result = query_result[0]

                with self.subTest(
                    msg="Given envelope name & database envelope name match."
                ):
                    self.assertEqual(result["name"], new_envelope["name"])
                with self.subTest(msg="Binds to currently auth'd user."):
                    self.assertEqual(result["user_id"], user_id)
                with self.subTest(msg="Starts with 0 funds."):
                    self.assertEqual(result["total_funds"], 0)


if __name__ == "__main__":
    main()
