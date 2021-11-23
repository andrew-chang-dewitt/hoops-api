"""Tests for /account routes."""

from typing import cast, Tuple
from uuid import UUID
from unittest import main, IsolatedAsyncioTestCase as TestCase

from db_wrapper.model import sql

# internal test dependencies
from src.database import Client
from tests.helpers.application import (
    get_test_client,
    get_token_header,
)

BASE_URL = "/account"


async def setup_user(database: Client) -> Tuple[UUID, UUID]:
    """Sets up database with 2 users for testing."""
    query = """
        INSERT INTO
            hoops_user(handle, full_name, preferred_name, password)
        VALUES
            ('user', 'A Full Name', 'Nickname', '@ new p4s5w0rd'),
            ('other', 'Other', 'Other', 'other')
        RETURNING id;
    """

    await database.connect()
    result = await database.execute_and_return(query)
    await database.disconnect()

    return cast(UUID, result[0]["id"]), cast(UUID, result[1]["id"])


class TestRoutePostRoot(TestCase):
    """Tests for `POST /account`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        new_account = {
            "name": "an account name"
        }

        async with get_test_client() as clients:
            client, database = clients
            user_id, _ = await setup_user(database)

            response = await client.post(
                BASE_URL,
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"},
                json=new_account)

            with self.subTest(
                    msg="Responds with a status code of 201."):
                self.assertEqual(201, response.status_code)

            with self.subTest(
                msg="Responds with new Account's id, name, & User id."
            ):
                body = response.json()

                with self.subTest():
                    self.assertTrue(UUID(body["id"]))
                with self.subTest():
                    self.assertEqual(body["name"], new_account["name"])
                with self.subTest():
                    self.assertEqual(UUID(body["user_id"]), user_id)

            with self.subTest(
                    msg="New Account is in the database."):
                body = response.json()
                new_id = UUID(body["id"])

                await database.connect()
                query_result = await database.execute_and_return(sql.SQL("""
                    SELECT * FROM account
                    WHERE id = {new_id};
                """).format(new_id=sql.Literal(new_id)))
                await database.disconnect()

                result = query_result[0]

                with self.subTest(
                    msg="Given account name & database account name match."
                ):
                    self.assertEqual(result["name"], new_account["name"])
                with self.subTest(
                        msg="Given User id & database User id match."):
                    self.assertEqual(result["user_id"], user_id)


class TestRouteGetRoot(TestCase):
    """Tests for `GET /account`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients
            user_id, other_id = await setup_user(database)

            query = sql.SQL("""
                INSERT INTO
                    account(name, user_id, closed)
                VALUES
                    ('other user account', {other_id}, false),
                    ('first account', {user_id}, false),
                    ('second account', {user_id}, false),
                    ('third account', {user_id}, false),
                    ('closed account', {user_id}, true);
            """).format(
                other_id=sql.Literal(other_id),
                user_id=sql.Literal(user_id))

            await database.connect()
            await database.execute(query)
            await database.disconnect()

            response = await client.get(
                BASE_URL,
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                    msg="Responds with list of accounts."):
                body = response.json()

                for item in body:
                    with self.subTest():
                        self.assertTrue(UUID(item["id"]))
                        self.assertTrue(item["name"])
                        self.assertTrue(item["user_id"])

            with self.subTest(
                msg="Only includes accounts belonging to the current user."
            ):
                for item in body:
                    with self.subTest():
                        self.assertEqual(user_id, UUID(item["user_id"]))

            with self.subTest(
                msg="Only includes open accounts."
            ):
                for item in body:
                    with self.subTest():
                        self.assertFalse(item["closed"])


class TestRoutePutId(TestCase):
    """Tests for `PUT /account/{id}`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients
            user_id, _ = await setup_user(database)

            query = sql.SQL("""
                INSERT INTO
                    account(name, user_id)
                VALUES
                    ('an account', {user_id})
                RETURNING id;
            """).format(user_id=sql.Literal(user_id))

            await database.connect()
            result = await database.execute_and_return(query)
            await database.disconnect()

            account_id = result[0]["id"]

            updates = {
                "name": "new account name"
            }

            response = await client.put(
                f"{BASE_URL}/{str(account_id)}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"},
                json=updates)

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(
                    200,
                    response.status_code,
                    msg=f"\nresponse: {response.json()}")

            with self.subTest(
                msg="Includes the updated Account."
            ):
                body = response.json()

                self.assertEqual(body["name"], updates["name"])

            with self.subTest(
                msg="Updates the account in the database"
            ):
                query = sql.SQL("""
                    SELECT *
                    FROM account
                    WHERE id = {account_id};
                """).format(account_id=sql.Literal(account_id))

                await database.connect()
                db_result = await database.execute_and_return(query)
                await database.disconnect()

                self.assertEqual(db_result[0]["name"], updates["name"])


class TestRoutePutClosed(TestCase):
    """Testing PUT /account/{id}/closed."""

    async def test_valid_request(self) -> None:
        """An account can be marked as closed."""
        async with get_test_client() as clients:
            client, database = clients
            user_id, _ = await setup_user(database)

            query = sql.SQL("""
                INSERT INTO
                    account(name, user_id)
                VALUES
                    ('an account', {user_id})
                RETURNING id;
            """).format(user_id=sql.Literal(user_id))

            await database.connect()
            result = await database.execute_and_return(query)
            await database.disconnect()

            account_id = result[0]["id"]

            response = await client.put(
                f"{BASE_URL}/{str(account_id)}/closed",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(
                    200,
                    response.status_code,
                    msg=f"\nresponse: {response.json()}")

            with self.subTest(msg="Returns the updated account."):
                body = response.json()

                self.assertEqual(True, body["closed"])

            with self.subTest(msg="Updates the Account in the database."):
                query = sql.SQL("""
                    SELECT *
                    FROM account
                    WHERE id = {account_id};
                """).format(
                    account_id=sql.Literal(account_id))

                await database.connect()
                result = await database.execute_and_return(query)
                await database.disconnect()

                in_db = result[0]

                self.assertEqual(True, in_db["closed"])


class TestRouteGetClosed(TestCase):
    """Tests for `GET /account/closed`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients
            user_id, other_id = await setup_user(database)

            query = sql.SQL("""
                INSERT INTO
                    account(name, user_id, closed)
                VALUES
                    ('first closed account', {user_id}, true),
                    ('second closed account', {user_id}, true),
                    ('open account', {user_id}, false);
            """).format(
                other_id=sql.Literal(other_id),
                user_id=sql.Literal(user_id))

            await database.connect()
            await database.execute(query)
            await database.disconnect()

            response = await client.get(
                f"{BASE_URL}/closed",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 201."):
                self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    main()
