"""Tests for /user routes."""

from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from uuid import UUID
from unittest import main, IsolatedAsyncioTestCase as TestCase

from db_wrapper.model import sql

# internal test dependencies
from tests.helpers.application import (
    get_test_client,
    get_token_header,
)
from src.database import Client

BASE_URL = "/transaction"


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
    result: List[Dict[str, UUID]] = await database.execute_and_return(query)
    await database.disconnect()

    return result[0]["id"], result[1]["id"]


async def setup_account(
    database: Client,
    user_id: Optional[UUID] = None
) -> UUID:
    """Sets up database with 1 account for given user for testing."""
    if not user_id:
        user_id = (await setup_user(database))[0]

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


class TestRoutePostRoot(TestCase):
    """Tests for `POST /transaction`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            user_id = (await setup_user(database))[0]
            account_id = await setup_account(database, user_id)

            new_transaction = {
                "amount": 1.23,
                "description": "a description",
                "payee": "payee",
                "timestamp": "2019-12-10T08:12-05:00",
                "account_id": str(account_id),
            }

            response = await client.post(
                BASE_URL,
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"},
                json=new_transaction)

            with self.subTest(
                    msg="Responds with a status code of 201."):
                self.assertEqual(201, response.status_code)

            with self.subTest(
                msg="Responds with new Transaction's information."
            ):
                body = response.json()

                with self.subTest():
                    self.assertTrue(UUID(body["id"]))
                with self.subTest():
                    self.assertEqual(body["amount"],
                                     new_transaction["amount"])
                with self.subTest():
                    self.assertEqual(body["description"],
                                     new_transaction["description"])
                with self.subTest():
                    self.assertEqual(body["payee"], new_transaction["payee"])
                with self.subTest():
                    self.assertEqual(
                        datetime.fromisoformat(body["timestamp"]),
                        datetime.fromisoformat(new_transaction["timestamp"]))
                with self.subTest():
                    self.assertEqual(body["account_id"],
                                     new_transaction["account_id"])

            with self.subTest(
                    msg="New Transaction is in the database."):
                body = response.json()
                new_id = UUID(body["id"])

                await database.connect()
                query_result = await database.execute_and_return(sql.SQL("""
                    SELECT * FROM transaction
                    WHERE id = {new_id};
                """).format(new_id=sql.Literal(new_id)))
                await database.disconnect()

                result = query_result[0]

                with self.subTest(
                    msg="Given transaction amount & database match."
                ):
                    self.assertEqual(result["amount"],
                                     Decimal(str(new_transaction["amount"])))
                with self.subTest(
                    msg="Given transaction payee & database match."
                ):
                    self.assertEqual(result["payee"], new_transaction["payee"])
                with self.subTest(
                    msg="Given transaction description & database match."
                ):
                    self.assertEqual(
                        result["description"], new_transaction["description"])
                with self.subTest(
                    msg="Given transaction timestamp & database match."
                ):
                    self.assertEqual(
                        result["timestamp"],
                        datetime.fromisoformat(new_transaction["timestamp"]))
                with self.subTest(
                    msg="Given transaction account_id & database match."
                ):
                    self.assertEqual(
                        result["account_id"],
                        UUID(new_transaction["account_id"]))

    async def test_cant_create_transactions_if_not_own_account(self) -> None:
        """Return 401 attempting to create transaction for other account."""
        async with get_test_client() as clients:
            client, database = clients

            user_id, other_user = (await setup_user(database))
            other_account = await setup_account(database, other_user)

            new_transaction = {
                "amount": 1.23,
                "description": "a description",
                "payee": "payee",
                "timestamp": "2019-12-10T08:12-05:00",
                "account_id": str(other_account),
            }

            response = await client.post(
                BASE_URL,
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"},
                json=new_transaction)

            self.assertEqual(401, response.status_code)


class TestRouteGetRoot(TestCase):
    """Tests for `GET /transaction`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = (await setup_user(database))[0]
            account_id = await setup_account(database, user_id)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description,
                                timestamp, account_id)
                VALUES
                    (1.23, 'a payee', 'a description',
                     {timestamp1}, {account_id}),
                    (1.23, 'a payee', 'a description',
                     {timestamp2}, {account_id}),
                    (1.23, 'a payee', 'a description',
                     {timestamp3}, {account_id});
            """).format(
                account_id=sql.Literal(account_id),
                timestamp1=sql.Literal("2019-12-10T08:12-05:00"),
                timestamp2=sql.Literal("2019-12-10T09:12-05:00"),
                timestamp3=sql.Literal("2019-12-11T06:12-05:00"),
            )
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

            with self.subTest(msg="All objects returned are Transactions."):
                for item in response.json():
                    with self.subTest(msg="Amount is float"):
                        self.assertTrue(isinstance(item["amount"], float))
                    with self.subTest(msg="Payee is string"):
                        self.assertTrue(isinstance(item["payee"], str))
                    with self.subTest(msg="Description is string"):
                        self.assertTrue(isinstance(item["description"], str))
                    with self.subTest(msg="Timestamp is ISO Datetime"):
                        self.assertTrue(
                            datetime.fromisoformat(item["timestamp"]))
                    with self.subTest(msg="Account ID is UUID"):
                        self.assertTrue(UUID(item["account_id"]))


class TestRoutePutId(TestCase):
    """Tests for `PUT /transaction/{id}`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = (await setup_user(database))[0]
            account_id = await setup_account(database, user_id)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description, timestamp, account_id)
                VALUES
                    (1.23, 'a payee', 'a description', {timestamp1}, {account_id})
                RETURNING id;
            """).format(
                account_id=sql.Literal(account_id),
                timestamp1=sql.Literal("2019-12-10T08:12-05:00"),
            )
            await database.connect()
            tran_id = (await database.execute_and_return(query))[0]["id"]
            await database.disconnect()

            changes = {
                "description": "something new",
            }

            response = await client.put(
                f"{BASE_URL}/{tran_id}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"},
                json=changes)

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                    msg="Returns the updated transaction."):
                body = response.json()

                self.assertEqual(body["description"], changes["description"])

            with self.subTest(msg="Updates the database."):
                new_id = UUID(body["id"])

                await database.connect()
                query_result = await database.execute_and_return(sql.SQL("""
                    SELECT * FROM transaction
                    WHERE id = {new_id};
                """).format(new_id=sql.Literal(new_id)))
                await database.disconnect()

                result = query_result[0]

                self.assertEqual(result["description"], changes["description"])

    async def test_cant_update_transactions_if_not_own_account(self) -> None:
        """Return 401 attempting to update transaction for other account."""
        async with get_test_client() as clients:
            client, database = clients

            user_id, other_user = (await setup_user(database))
            other_account = await setup_account(database, other_user)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description, timestamp, account_id)
                VALUES
                    (1.23, 'a payee', 'a description', {timestamp1}, {account_id})
                RETURNING id;
            """).format(
                account_id=sql.Literal(other_account),
                timestamp1=sql.Literal("2019-12-10T08:12-05:00"),
            )
            await database.connect()
            tran_id = (await database.execute_and_return(query))[0]["id"]
            await database.disconnect()

            changes = {
                "description": "new description",
            }

            response = await client.put(
                f"{BASE_URL}/{tran_id}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"},
                json=changes)

            self.assertEqual(401, response.status_code)


class TestRouteDeleteId(TestCase):
    """Test DELETE /transaction/{id}."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = (await setup_user(database))[0]
            account_id = await setup_account(database, user_id)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description, timestamp, account_id)
                VALUES
                    (1.23, 'a payee', 'a description', {timestamp1}, {account_id})
                RETURNING id;
            """).format(
                account_id=sql.Literal(account_id),
                timestamp1=sql.Literal("2019-12-10T08:12-05:00"),
            )
            await database.connect()
            tran_id = (await database.execute_and_return(query))[0]["id"]
            await database.disconnect()

            response = await client.delete(
                f"{BASE_URL}/{tran_id}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

    async def test_cant_delete_transactions_if_not_own_account(self) -> None:
        """Return 401 attempting to delete transaction for other account."""
        async with get_test_client() as clients:
            client, database = clients

            user_id, other_user = (await setup_user(database))
            other_account = await setup_account(database, other_user)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description, timestamp, account_id)
                VALUES
                    (1.23, 'a payee', 'a description', {timestamp1}, {account_id})
                RETURNING id;
            """).format(
                account_id=sql.Literal(other_account),
                timestamp1=sql.Literal("2019-12-10T08:12-05:00"),
            )
            await database.connect()
            tran_id = (await database.execute_and_return(query))[0]["id"]
            await database.disconnect()

            response = await client.delete(
                f"{BASE_URL}/{tran_id}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            self.assertEqual(401, response.status_code)


if __name__ == "__main__":
    main()
