"""Tests for /transaction routes."""

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
from tests.helpers.database import setup_user, setup_account
from src.database import Client

BASE_URL = "/transaction"


class TestRoutePostRoot(TestCase):
    """Tests for `POST /transaction`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            user_id = await setup_user(database)
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
        """Return 403 attempting to create transaction for other account."""
        async with get_test_client() as clients:
            client, database = clients

            user_id = await setup_user(database, "user")
            other_user = await setup_user(database, "other")
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

            self.assertEqual(403, response.status_code)


class TestRouteGetRoot(TestCase):
    """Tests for `GET /transaction`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
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

    async def test_filter_by_account(self) -> None:
        """Requests can filter by account."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
            account1 = await setup_account(database, user_id)
            account2 = await setup_account(database, user_id)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description,
                                timestamp, account_id)
                VALUES
                    (1.23, 'a payee', 'a description',
                     {timestamp1}, {account1}),
                    (1.23, 'a payee', 'a description',
                     {timestamp1}, {account2});
            """).format(
                account1=sql.Literal(account1),
                account2=sql.Literal(account2),
                timestamp1=sql.Literal("2019-12-10T08:12-05:00"),
            )
            await database.connect()
            await database.execute(query)
            await database.disconnect()

            response = await client.get(
                f"{BASE_URL}?account_id={account1}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                msg="Only returns Transactions belonging to requested Account."
            ):
                for transaction in response.json():
                    self.assertEqual(transaction["account_id"], str(account1))

    async def test_filter_payee(self) -> None:
        """Requests can filter by payee."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
            account1 = await setup_account(database, user_id)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description,
                                timestamp, account_id)
                VALUES
                    (1.23, 'a payee', 'a description',
                     {timestamp1}, {account1}),
                    (1.23, 'someone else', 'a description',
                     {timestamp1}, {account1});
            """).format(
                account1=sql.Literal(account1),
                timestamp1=sql.Literal("2019-12-10T08:12-05:00"),
            )
            await database.connect()
            await database.execute(query)
            await database.disconnect()

            response = await client.get(
                f"{BASE_URL}?payee=a%20payee",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                msg="Only returns Transactions with matching payee."
            ):
                for transaction in response.json():
                    self.assertEqual(transaction["payee"], str("a payee"))

    async def test_filter_minimum_amount(self) -> None:
        """Requests can filter by minimum amount."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
            account1 = await setup_account(database, user_id)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description,
                                timestamp, account_id)
                VALUES
                    (1.23, 'a payee', 'a description',
                     {timestamp1}, {account1}),
                    (0.23, 'a payee', 'a description',
                     {timestamp1}, {account1});
            """).format(
                account1=sql.Literal(account1),
                timestamp1=sql.Literal("2019-12-10T08:12-05:00"),
            )
            await database.connect()
            await database.execute(query)
            await database.disconnect()

            response = await client.get(
                f"{BASE_URL}?minimum_amount=1.00",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                    msg="Only returns Transactions >= to given amount."):
                for transaction in response.json():
                    self.assertGreaterEqual(transaction["amount"], 1)

    async def test_filter_maximum_amount(self) -> None:
        """Requests can filter by maximum amount."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
            account1 = await setup_account(database, user_id)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description,
                                timestamp, account_id)
                VALUES
                    (1.23, 'a payee', 'a description',
                     {timestamp1}, {account1}),
                    (0.23, 'a payee', 'a description',
                     {timestamp1}, {account1});
            """).format(
                account1=sql.Literal(account1),
                timestamp1=sql.Literal("2019-12-10T08:12-05:00"),
            )
            await database.connect()
            await database.execute(query)
            await database.disconnect()

            response = await client.get(
                f"{BASE_URL}?maximum_amount=1.00",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                    msg="Only returns Transactions >= to given amount."):
                for transaction in response.json():
                    self.assertLessEqual(transaction["amount"], 1)

    async def test_filter_minumum_and_maximum_amount(self) -> None:
        """Requests can filter by both minimum and maximum amount."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
            account1 = await setup_account(database, user_id)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description,
                                timestamp, account_id)
                VALUES
                    (1.23, 'a payee', 'a description',
                     {timestamp1}, {account1}),
                    (0.23, 'a payee', 'a description',
                     {timestamp1}, {account1}),
                    (-1.00, 'a payee', 'a description',
                     {timestamp1}, {account1});
            """).format(
                account1=sql.Literal(account1),
                timestamp1=sql.Literal("2019-12-10T08:12-05:00"),
            )
            await database.connect()
            await database.execute(query)
            await database.disconnect()

            response = await client.get(
                f"{BASE_URL}?minimum_amount=0.00&maximum_amount=1.00",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                msg="Only returns Transactions inclusive between amounts."
            ):
                body = response.json()
                print(f"\n\nresponse body: {body}")
                for transaction in body:
                    with self.subTest(msg="Greater than/equal to minimum."):
                        self.assertGreaterEqual(transaction["amount"], 0)
                    with self.subTest(msg="Less than/equal to maximum."):
                        self.assertLessEqual(transaction["amount"], 1)

    async def test_filter_minimum_timestamp(self) -> None:
        """Requests can filter by minimum timestamp."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
            account1 = await setup_account(database, user_id)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description,
                                timestamp, account_id)
                VALUES
                    (1, 'a payee', 'a description',
                     {timestamp1}, {account1}),
                    (1, 'a payee', 'a description',
                     {timestamp2}, {account1});
            """).format(
                account1=sql.Literal(account1),
                timestamp1=sql.Literal("2019-12-10T08:12-05:00"),
                timestamp2=sql.Literal("2020-12-10T08:12-05:00"),
            )
            await database.connect()
            await database.execute(query)
            await database.disconnect()

            after = "2020-01-01T00:00-00:00"
            response = await client.get(
                f"{BASE_URL}?after={after}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                    msg="Only returns Transactions >= to given timestamp."):
                for transaction in response.json():
                    self.assertGreaterEqual(
                        datetime.fromisoformat(transaction["timestamp"]),
                        datetime.fromisoformat(after))

    async def test_filter_maximum_timestamp(self) -> None:
        """Requests can filter by maximum timestamp."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
            account1 = await setup_account(database, user_id)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description,
                                timestamp, account_id)
                VALUES
                    (1, 'a payee', 'a description',
                     {timestamp1}, {account1}),
                    (1, 'a payee', 'a description',
                     {timestamp2}, {account1});
            """).format(
                account1=sql.Literal(account1),
                timestamp1=sql.Literal("2019-12-10T08:12-05:00"),
                timestamp2=sql.Literal("2020-12-10T08:12-05:00"),
            )
            await database.connect()
            await database.execute(query)
            await database.disconnect()

            before = "2020-01-01T00:00-00:00"
            response = await client.get(
                f"{BASE_URL}?before={before}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                    msg="Only returns Transactions >= to given timestamp."):
                for transaction in response.json():
                    self.assertLessEqual(
                        datetime.fromisoformat(transaction["timestamp"]),
                        datetime.fromisoformat(before))

    async def test_filter_minumum_and_maximum_timestamp(self) -> None:
        """Requests can filter by both minimum and maximum timestamp."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
            account1 = await setup_account(database, user_id)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description,
                                timestamp, account_id)
                VALUES
                    (1, 'a payee', 'a description',
                     {timestamp1}, {account1}),
                    (1, 'a payee', 'a description',
                     {timestamp2}, {account1}),
                    (1, 'a payee', 'a description',
                     {timestamp3}, {account1});
            """).format(
                account1=sql.Literal(account1),
                timestamp1=sql.Literal("2019-12-10T08:12-05:00"),
                timestamp2=sql.Literal("2020-12-10T08:12-05:00"),
                timestamp3=sql.Literal("2021-12-10T08:12-05:00"),
            )
            await database.connect()
            await database.execute(query)
            await database.disconnect()

            after = "2020-01-01T00:00-00:00"
            before = "2021-01-01T00:00-00:00"
            response = await client.get(
                f"{BASE_URL}?after={after}&before={before}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                    msg="Only returns Transactions >= to given timestamp."):
                for transaction in response.json():
                    self.assertLessEqual(
                        datetime.fromisoformat(transaction["timestamp"]),
                        datetime.fromisoformat(before))
            with self.subTest(
                msg="Only returns Transactions inclusive between timestamps."
            ):
                body = response.json()
                print(f"\n\nresponse body: {body}")
                for transaction in body:
                    with self.subTest(msg="Greater than/equal to minimum."):
                        self.assertGreaterEqual(
                            datetime.fromisoformat(transaction["timestamp"]),
                            datetime.fromisoformat(after))
                    with self.subTest(msg="Less than/equal to maximum."):
                        self.assertLessEqual(
                            datetime.fromisoformat(transaction["timestamp"]),
                            datetime.fromisoformat(before))

    async def test_pagination(self) -> None:
        """Requests can be paginated with number of results & page number."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
            account1 = await setup_account(database, user_id)
            query = sql.SQL("""
                INSERT INTO
                    transaction(amount, payee, description,
                                timestamp, account_id)
                VALUES
                    (1, 'a payee', 'a description',
                     {timestamp0}, {account1}),
                    (1, 'a payee', 'a description',
                     {timestamp1}, {account1}),
                    (1, 'a payee', 'a description',
                     {timestamp2}, {account1}),
                    (1, 'a payee', 'a description',
                     {timestamp3}, {account1}),
                    (1, 'a payee', 'a description',
                     {timestamp4}, {account1}),
                    (1, 'a payee', 'a description',
                     {timestamp5}, {account1}),
                    (1, 'a payee', 'a description',
                     {timestamp6}, {account1}),
                    (1, 'a payee', 'a description',
                     {timestamp7}, {account1}),
                    (1, 'a payee', 'a description',
                     {timestamp8}, {account1}),
                    (1, 'a payee', 'a description',
                     {timestamp9}, {account1});
            """).format(
                account1=sql.Literal(account1),
                timestamp0=sql.Literal("2019-12-10T08:12-05:00"),
                timestamp1=sql.Literal("2019-12-10T08:13-05:00"),
                timestamp2=sql.Literal("2019-12-10T08:14-05:00"),
                timestamp3=sql.Literal("2019-12-10T08:15-05:00"),
                timestamp4=sql.Literal("2019-12-10T08:16-05:00"),
                timestamp5=sql.Literal("2019-12-10T08:17-05:00"),
                timestamp6=sql.Literal("2019-12-10T08:18-05:00"),
                timestamp7=sql.Literal("2019-12-10T08:19-05:00"),
                timestamp8=sql.Literal("2019-12-10T08:20-05:00"),
                timestamp9=sql.Literal("2019-12-10T08:21-05:00"),
            )
            await database.connect()
            await database.execute(query)
            await database.disconnect()

            limit = 5
            page1 = 0
            response1 = await client.get(
                f"{BASE_URL}?limit={limit}&page={page1}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response1.status_code)

            with self.subTest(
                msg="Responds with number of Transactions specified by limit."
            ):
                body1 = response1.json()

                self.assertEqual(len(body1), limit)

            with self.subTest(
                    msg=f"Can get next {limit} Transactions using page."):
                page2 = 1
                response2 = await client.get(
                    f"{BASE_URL}?limit={limit}&page={page2}",
                    headers={
                        **get_token_header(user_id),
                        "accept": "application/json"})
                body2 = response2.json()

                first_page = [tran1["id"] for tran1 in body1]

                for tran in body2:
                    with self.subTest():
                        self.assertNotIn(tran["id"], first_page)


class TestRoutePutId(TestCase):
    """Tests for `PUT /transaction/{id}`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
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
        """Return 403 attempting to update transaction for other account."""
        async with get_test_client() as clients:
            client, database = clients

            user_id = await setup_user(database, "user")
            other_user = await setup_user(database, "other")
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

            self.assertEqual(403, response.status_code)


class TestRouteDeleteId(TestCase):
    """Test DELETE /transaction/{id}."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
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
        """Return 403 attempting to delete transaction for other account."""
        async with get_test_client() as clients:
            client, database = clients

            user_id = await setup_user(database, "user")
            other_user = await setup_user(database, "other")
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

            self.assertEqual(403, response.status_code)


if __name__ == "__main__":
    main()
