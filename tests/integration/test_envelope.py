"""Tests for /envelope routes."""

from decimal import Decimal
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


class TestRouteGetRoot(TestCase):
    """Testing GET /envelope."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            user_id = await setup_user(database, "first")
            other_id = await setup_user(database, "other")

            add_envelope_query = sql.SQL("""
                INSERT INTO envelope
                    (name, total_funds, user_id)
                VALUES
                    ('envelope', 1.00, {user_id}),
                    ('envelope', 1.00, {user_id}),
                    ('envelope', 1.00, {user_id}),
                    ('envelope', 1.00, {other_id});
            """).format(
                user_id=sql.Literal(user_id),
                other_id=sql.Literal(other_id))

            await database.connect()
            await database.execute(add_envelope_query)
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
                msg="Responds w/ all Envelopes belonging to current user."
            ):
                body = response.json()

                self.assertEqual(
                    len(body), 3, msg="Body should contain 3 Envelopes.")

                for item in body:
                    with self.subTest(msg="Envelope has a name."):
                        self.assertEqual(item["name"], "envelope")
                    with self.subTest(
                            msg="Bound to current user in auth token."):
                        self.assertEqual(item["user_id"], str(user_id))
                    with self.subTest(msg="Envelope has a UUID identifier."):
                        self.assertTrue(UUID(item["id"]))
                    with self.subTest(msg="Envelope has funds."):
                        self.assertEqual(item["total_funds"], 1.00)


class TestRouteGetId(TestCase):
    """Testing GET /envelope/{id}."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            user_id = await setup_user(database, "first")

            add_envelope_query = sql.SQL("""
                INSERT INTO envelope
                    (name, total_funds, user_id)
                VALUES
                    ('envelope', 1.00, {user_id})
                RETURNING
                    id;
            """).format(
                user_id=sql.Literal(user_id))

            await database.connect()
            query_result = \
                await database.execute_and_return(add_envelope_query)
            await database.disconnect()
            envelope_id = query_result[0]["id"]

            response = await client.get(
                f"{BASE_URL}/{envelope_id}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                    msg="Responds with requested Envelope's data."):
                body = response.json()

                with self.subTest(msg="Includes the Envelope's name."):
                    self.assertEqual(body["name"], "envelope")
                with self.subTest(msg="Bound to current user in auth token."):
                    self.assertEqual(body["user_id"], str(user_id))
                with self.subTest(msg="Has a UUID identifier."):
                    self.assertEqual(body["id"], str(envelope_id))
                with self.subTest(msg="Includes Envelope's funds."):
                    self.assertEqual(body["total_funds"], 1)

    async def test_can_only_get_own_envelopes(self) -> None:
        """A User can't get another User's Envelopes."""
        async with get_test_client() as clients:
            client, database = clients

            user_id = await setup_user(database, "first")
            other_id = await setup_user(database, "other")

            add_envelope_query = sql.SQL("""
                INSERT INTO envelope
                    (name, total_funds, user_id)
                VALUES
                    ('envelope', 1.00, {user_id})
                RETURNING
                    id;
            """).format(
                user_id=sql.Literal(user_id))

            await database.connect()
            query_result = \
                await database.execute_and_return(add_envelope_query)
            await database.disconnect()
            envelope_id = query_result[0]["id"]

            response = await client.get(
                f"{BASE_URL}/{envelope_id}",
                headers={
                    **get_token_header(other_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 404."):
                self.assertEqual(404, response.status_code)


class TestRoutePutId(TestCase):
    """Testing PUT /envelope/{id}."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        async with get_test_client() as clients:
            client, database = clients

            user_id = await setup_user(database, "first")

            add_envelope_query = sql.SQL("""
                INSERT INTO envelope
                    (name, total_funds, user_id)
                VALUES
                    ('envelope', 1.00, {user_id})
                RETURNING
                    id;
            """).format(
                user_id=sql.Literal(user_id))

            await database.connect()
            query_result = \
                await database.execute_and_return(add_envelope_query)
            await database.disconnect()
            envelope_id = query_result[0]["id"]

            changes = {"name": "new name"}

            response = await client.put(
                f"{BASE_URL}/{envelope_id}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"},
                json=changes)

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                    msg="Responds with requested Envelope's updated data."):
                body = response.json()

                with self.subTest(msg="Includes the Envelope's name."):
                    self.assertEqual(body["name"], changes["name"])

            with self.subTest(msg="Saves changes to the database."):
                body = response.json()
                new_id = UUID(body["id"])

                await database.connect()
                query_result = await database.execute_and_return(sql.SQL("""
                    SELECT * FROM envelope
                    WHERE id = {new_id};
                """).format(new_id=sql.Literal(new_id)))
                await database.disconnect()

                result = query_result[0]

                self.assertEqual(result["name"], changes["name"])

    async def test_can_only_change_own_envelopes(self) -> None:
        """A User can't change another User's Envelopes."""
        async with get_test_client() as clients:
            client, database = clients

            user_id = await setup_user(database, "first")
            other_id = await setup_user(database, "other")

            add_envelope_query = sql.SQL("""
                INSERT INTO envelope
                    (name, total_funds, user_id)
                VALUES
                    ('envelope', 1.00, {user_id})
                RETURNING
                    id;
            """).format(
                user_id=sql.Literal(user_id))

            await database.connect()
            query_result = \
                await database.execute_and_return(add_envelope_query)
            await database.disconnect()
            envelope_id = query_result[0]["id"]

            changes = {"name": "new name"}

            response = await client.put(
                f"{BASE_URL}/{envelope_id}",
                headers={
                    **get_token_header(other_id),
                    "accept": "application/json"},
                json=changes)

            with self.subTest(
                    msg="Responds with a status code of 404."):
                self.assertEqual(404, response.status_code)

    async def test_can_not_update_funds(self) -> None:
        """Funds must be updated via `.../funds/{amount}` endpoint."""
        self.assertTrue(False, "Not yet implemented.")


class TestRoutePutFunds(TestCase):
    """Testing PUT /envelope/{id}/funds/{amount}."""

    async def test_move_funds_from_available(self) -> None:
        """Testing moving funds from Available Balance."""
        async with get_test_client() as clients:
            client, database = clients

            user_id = await setup_user(database, "first")
            account_id = await setup_account(database, user_id)
            await setup_transactions(database, [Decimal(10)], account_id)

            add_envelope_query = sql.SQL("""
                INSERT INTO envelope
                    (name, total_funds, user_id)
                VALUES
                    ('envelope', 0.00, {user_id})
                RETURNING
                    id;
            """).format(
                user_id=sql.Literal(user_id))

            await database.connect()
            query_result = \
                await database.execute_and_return(add_envelope_query)
            await database.disconnect()
            envelope_id = query_result[0]["id"]

            amount = 5
            response = await client.put(
                f"{BASE_URL}/{envelope_id}/funds/{amount}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                    msg="Responds with Envelope with updated funds."):
                body = response.json()

                self.assertEqual(body["total_funds"], 5)

            with self.subTest(
                    msg="Envelope is updated in database."):
                query = sql.SQL("""
                    SELECT total_funds
                    FROM envelope
                    WHERE id = {envelope_id};
                """).format(
                    envelope_id=sql.Literal(envelope_id))

                await database.connect()
                query_result = await database.execute_and_return(query)
                await database.disconnect()

                self.assertEqual(query_result[0]["total_funds"], 5)

            with self.subTest(
                    msg="Can not move funds if not enough are available."):
                amount = 11
                response = await client.put(
                    f"{BASE_URL}/{envelope_id}/funds/{amount}",
                    headers={
                        **get_token_header(user_id),
                        "accept": "application/json"})

                self.assertEqual(response.status_code, 409)

    async def test_move_funds_from_other_envelope(self) -> None:
        """Testing moving funds from a given Envelope."""
        async with get_test_client() as clients:
            client, database = clients

            user_id = await setup_user(database, "first")
            account_id = await setup_account(database, user_id)
            await setup_transactions(database, [Decimal(10)], account_id)

            add_envelopes_query = sql.SQL("""
                INSERT INTO envelope
                    (name, total_funds, user_id)
                VALUES
                    ('to', 0.00, {user_id}),
                    ('from', 10.00, {user_id})
                RETURNING
                    id, name;
            """).format(
                user_id=sql.Literal(user_id))

            await database.connect()
            query_result = \
                await database.execute_and_return(add_envelopes_query)
            await database.disconnect()

            for result in query_result:
                if result["name"] == "from":
                    from_envelope = result["id"]
                if result["name"] == "to":
                    to_envelope = result["id"]

            amount = 5
            response = await client.put(
                f"{BASE_URL}/{to_envelope}/funds/{amount}" +
                f"?source={from_envelope}",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                    msg="Source Envelope is updated in database."):
                query = sql.SQL("""
                    SELECT total_funds
                    FROM envelope
                    WHERE id = {from_envelope};
                """).format(
                    from_envelope=sql.Literal(from_envelope))

                await database.connect()
                query_result = await database.execute_and_return(query)
                await database.disconnect()

                self.assertEqual(query_result[0]["total_funds"], 5)

            with self.subTest(
                    msg="Can not move funds if not enough are available."):
                amount = 11
                response = await client.put(
                    f"{BASE_URL}/{to_envelope}/funds/{amount}" +
                    f"?source={from_envelope}",
                    headers={
                        **get_token_header(user_id),
                        "accept": "application/json"})

                self.assertEqual(response.status_code, 409)


if __name__ == "__main__":
    main()
