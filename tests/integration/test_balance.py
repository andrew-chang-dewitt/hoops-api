"""Tests for /balance routes."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from unittest import main, IsolatedAsyncioTestCase as TestCase
from uuid import UUID

from db_wrapper.model import sql

# internal test dependencies
from tests.helpers.application import (
    get_test_client,
    get_token_header,
)
from tests.helpers.database import setup_user, setup_account
from src.database import Client

BASE_URL = "/balance"


def _build_transaction(
    account_id: UUID,
    amount: Decimal = Decimal("1.00"),
    payee: str = "payee",
    description: str = "description",
    timestamp: datetime = datetime.fromisoformat("2019-12-10T08:12-05:00"),
    spent_from: Optional[UUID] = None,
) -> sql.Composed:
    return sql.SQL("""
        ({amount},
         {payee},
         {description},
         {timestamp},
         {account_id},
         {spent_from})
    """).format(
        account_id=sql.Literal(account_id),
        amount=sql.Literal(amount),
        payee=sql.Literal(payee),
        description=sql.Literal(description),
        timestamp=sql.Literal(timestamp),
        spent_from=sql.Literal(spent_from))


async def setup_transactions(
    database: Client,
    values: List[Dict[str, Any]],
    account_id: UUID,
) -> None:
    """Sets up database with transactions of given properties."""
    query = sql.SQL("""
        INSERT INTO
            transaction(
                amount,
                payee,
                description,
                timestamp,
                account_id,
                spent_from)
        VALUES {transactions};
    """).format(
        transactions=sql.SQL(",").join(
            [_build_transaction(account_id, **value) for value in values]))

    await database.connect()
    await database.execute(query)
    await database.disconnect()


async def setup_envelope(
        database: Client,
        user_id: UUID,
        name: str = "name",
        funds: Decimal = Decimal(0),
) -> UUID:
    """Sets up database with Envelopes using given name & user."""
    query = sql.SQL("""
        INSERT INTO envelope(name, user_id, total_funds)
        VALUES ({name}, {user_id}, {total_funds})
        RETURNING id;
    """).format(
        name=sql.Literal(name),
        user_id=sql.Literal(user_id),
        total_funds=sql.Literal(funds))

    await database.connect()
    query_result = await database.execute_and_return(query)
    await database.disconnect()

    result: UUID = query_result[0]["id"]

    return result


class TestRouteGetTotal(TestCase):
    """Testing GET /balance/total."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
            account1_id = await setup_account(database, user_id)
            await setup_transactions(
                database,
                [
                    {"amount": Decimal(1)},
                    {"amount": Decimal(2)},
                    {"amount": Decimal(3)},
                    {"amount": Decimal(4)},
                    {"amount": Decimal(5)},
                    {"amount": Decimal(6)},
                    {"amount": Decimal(7)},
                    {"amount": Decimal(8)},
                    {"amount": Decimal(9)},
                    {"amount": Decimal(10)},
                ],
                account1_id)

            account2_id = await setup_account(database, user_id)
            await setup_transactions(
                database,
                [
                    {"amount": Decimal(11)},
                    {"amount": Decimal(12)},
                    {"amount": Decimal(13)},
                    {"amount": Decimal(14)},
                    {"amount": Decimal(15)},
                    {"amount": Decimal(16)},
                    {"amount": Decimal(17)},
                    {"amount": Decimal(18)},
                    {"amount": Decimal(19)},
                    {"amount": Decimal(20)},
                ],
                account2_id)

            response = await client.get(
                f"{BASE_URL}/total",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                msg="Response has sum of Transaction amounts for all accounts."
            ):
                body = response.json()

                self.assertEqual(body["amount"], 210)


class TestRouteGetAccount(TestCase):
    """Testing GET /balance/account/{id}."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
            account_id = await setup_account(database, user_id)
            await setup_transactions(
                database,
                [
                    {"amount": Decimal(1)},
                    {"amount": Decimal(2)},
                    {"amount": Decimal(3)},
                    {"amount": Decimal(4)},
                    {"amount": Decimal(5)},
                    {"amount": Decimal(6)},
                    {"amount": Decimal(7)},
                    {"amount": Decimal(8)},
                    {"amount": Decimal(9)},
                    {"amount": Decimal(10)},
                ],
                account_id)

            response = await client.get(
                f"{BASE_URL}/account/{account_id}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(msg="Response contains name of account."):
                body = response.json()

                self.assertEqual(body["collection"], "an account")

            with self.subTest(
                    msg="Response contains sum of Transaction amounts."):
                body = response.json()

                self.assertEqual(body["amount"], 55)


class TestRouteGetEnvelope(TestCase):
    """Testing GET /balance/envelope."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
            account_id = await setup_account(database, user_id)
            envelope1 = await setup_envelope(database,
                                             user_id,
                                             funds=Decimal(100))
            await setup_transactions(
                database,
                [
                    {"amount": Decimal(-1), "spent_from": envelope1},
                    {"amount": Decimal(-2), "spent_from": envelope1},
                    {"amount": Decimal(-3), "spent_from": envelope1},
                    {"amount": Decimal(-4), "spent_from": envelope1},
                    {"amount": Decimal(-5), "spent_from": envelope1},
                    {"amount": Decimal(-6), "spent_from": envelope1},
                    {"amount": Decimal(-7), "spent_from": envelope1},
                    {"amount": Decimal(-8), "spent_from": envelope1},
                    {"amount": Decimal(-9), "spent_from": envelope1},
                    {"amount": Decimal(-10), "spent_from": envelope1},
                ],
                account_id)

            response = await client.get(
                f"{BASE_URL}/envelope/{envelope1}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                msg="Balance is total funds - sum of Transactions spent."
            ):
                body = response.json()
                print(f"body: {body}")

                self.assertEqual(body["amount"], 45)


class TestRouteGetAvailable(TestCase):

    """Testing GET /balance/available."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = await setup_user(database)
            account_id = await setup_account(database, user_id)
            envelope1 = await setup_envelope(database, user_id, funds=Decimal(5))
            envelope2 = await setup_envelope(database, user_id, funds=Decimal(10))
            await setup_transactions(
                database,
                [
                    {"amount": Decimal(-1), "spent_from": envelope1},
                    {"amount": Decimal(-2)},
                    {"amount": Decimal(-3)},
                    {"amount": Decimal(-4)},
                    {"amount": Decimal(-5)},
                    {"amount": Decimal(-6)},
                    {"amount": Decimal(-7)},
                    {"amount": Decimal(-8)},
                    {"amount": Decimal(-9)},
                    {"amount": Decimal(-10), "spent_from": envelope2},
                    {"amount": Decimal(100)},
                ],
                account_id)

            response = await client.get(
                f"{BASE_URL}/available",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                msg="Available balance is total - unspent amount in Envelopes."
            ):
                body = response.json()
                print(f"body: {body}")

                self.assertEqual(body["amount"], 41)


if __name__ == "__main__":
    main()
