"""Tests for /balance routes."""

from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from unittest import main, IsolatedAsyncioTestCase as TestCase
from uuid import UUID

from db_wrapper.model import sql

# internal test dependencies
from tests.helpers.application import (
    get_test_client,
    get_token_header,
)
from src.database import Client

BASE_URL = "/balance"


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


async def setup_transactions(
    database: Client,
    amounts: List[Decimal],
    account_id: Optional[UUID] = None,
) -> None:
    """Sets up database with transactions of given amounts."""
    if not account_id:
        account_id = await setup_account(database)

    def build_transaction(amount: Decimal) -> sql.Composed:
        return sql.SQL("""
            ({amount},
             'payee',
             'description',
             '2019-12-10T08:12-05:00',
             {account_id})
        """).format(
            amount=sql.Literal(amount),
            account_id=sql.Literal(account_id))

    query = sql.SQL("""
        INSERT INTO
            transaction(amount, payee, description, timestamp, account_id)
        VALUES {amounts};
    """).format(
        amounts=sql.SQL(",").join(
            [build_transaction(amount) for amount in amounts]))

    await database.connect()
    await database.execute(query)
    await database.disconnect()


class TestRouteGetTotal(TestCase):
    """Testing GET /balance/total."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            # insert some test transactions
            user_id = (await setup_user(database))[0]
            account1_id = await setup_account(database, user_id)
            await setup_transactions(
                database,
                [
                    Decimal(1),
                    Decimal(2),
                    Decimal(3),
                    Decimal(4),
                    Decimal(5),
                    Decimal(6),
                    Decimal(7),
                    Decimal(8),
                    Decimal(9),
                    Decimal(10),
                ],
                account1_id)

            account2_id = await setup_account(database, user_id)
            await setup_transactions(
                database,
                [
                    Decimal(11),
                    Decimal(12),
                    Decimal(13),
                    Decimal(14),
                    Decimal(15),
                    Decimal(16),
                    Decimal(17),
                    Decimal(18),
                    Decimal(19),
                    Decimal(20),
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
            user_id = (await setup_user(database))[0]
            account_id = await setup_account(database, user_id)
            await setup_transactions(
                database,
                [
                    Decimal(1),
                    Decimal(2),
                    Decimal(3),
                    Decimal(4),
                    Decimal(5),
                    Decimal(6),
                    Decimal(7),
                    Decimal(8),
                    Decimal(9),
                    Decimal(10),
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


if __name__ == "__main__":
    main()
