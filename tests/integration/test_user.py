"""Tests for /user routes."""

from uuid import UUID
from unittest import main, IsolatedAsyncioTestCase as TestCase

from db_wrapper.model import sql

# internal test dependencies
from tests.helpers.application import (
    get_test_client,
    get_token_header,
)


class TestRoutePostRoot(TestCase):
    """Tests for `POST /user`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        new_user = {
            "handle": "new_user",
            "password": "@ new p4s5w0rd",
            "full_name": "A Full Name",
            "preferred_name": "Nickname",
        }

        async with get_test_client() as clients:
            client, database = clients

            response = await client.post(
                "/user",
                json=new_user)

            with self.subTest(
                    msg="Responds with a status code of 201."):
                self.assertEqual(201, response.status_code)

            with self.subTest(
                msg="Responds with newly created User's handle, names, & ID."
            ):
                body = response.json()

                with self.subTest():
                    self.assertTrue(UUID(body["id"]))
                with self.subTest():
                    self.assertEqual(body["handle"], new_user["handle"])
                with self.subTest():
                    self.assertEqual(body["full_name"], new_user["full_name"])
                with self.subTest():
                    self.assertEqual(body["preferred_name"],
                                     new_user["preferred_name"])
                with self.subTest(
                        msg="Response body does not include new password."):
                    self.assertNotIn("password", body.keys())

            with self.subTest(
                    msg="New User is in the database."):
                body = response.json()
                new_id = UUID(body["id"])

                await database.connect()
                query_result = await database.execute_and_return(sql.SQL("""
                    SELECT * FROM hoops_user
                    WHERE id = {new_id};
                """).format(new_id=sql.Literal(new_id)))
                await database.disconnect()

                result = query_result[0]

                with self.subTest(
                        msg="Given handle & database handle match."):
                    self.assertEqual(result["handle"], new_user["handle"])
                with self.subTest(
                        msg="Given full name & database full name match."):
                    self.assertEqual(
                        result["full_name"], new_user["full_name"])
                with self.subTest(
                        msg="Given preferred name & matches db."):
                    self.assertEqual(
                        result["preferred_name"], new_user["preferred_name"])
                with self.subTest(
                        msg="Given password is encrypted before storing."):
                    self.assertNotEqual(
                        result["password"], new_user["password"])

    async def test_user_already_exists(self) -> None:
        """Returns 409 if user already exists."""
        new_user = {
            "handle": "new_user",
            "password": "@ new p4s5w0rd",
            "full_name": "A Full Name",
            "preferred_name": "Nickname",
        }

        async with get_test_client() as clients:
            client, database = clients

            # create existing user
            await database.connect()
            await database.execute("""
                INSERT INTO hoops_user(handle, full_name, password)
                VALUES ('new_user', 'A Name', 'password');
            """)
            await database.disconnect()

            # attempt to add new user with same handle
            response = await client.post(
                "/user",
                json=new_user)

            self.assertEqual(409, response.status_code)


class TestRouteGetRoot(TestCase):
    """Tests for `GET /user`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        query = """
            INSERT INTO
                hoops_user(handle, full_name, preferred_name, password)
            VALUES
                ('user', 'A Full Name', 'Nickname', '@ new p4s5w0rd')
            RETURNING id;
        """

        async with get_test_client() as clients:
            client, database = clients

            await database.connect()
            result = await database.execute_and_return(query)
            await database.disconnect()

            user_id = result[0]["id"]

            response = await client.get(
                "/user",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                msg="Responds with Content-Type: application/json Header."
            ):
                self.assertEqual(response.headers.get(
                    'content-type'), 'application/json')

            with self.subTest(
                    msg="Responds with authorized User's data."):
                body = response.json()

                with self.subTest():
                    self.assertEqual(body["id"], str(user_id))
                with self.subTest():
                    self.assertEqual(body['handle'], "user")
                with self.subTest():
                    self.assertEqual(body['full_name'], "A Full Name")
                with self.subTest():
                    self.assertEqual(body['preferred_name'], "Nickname")

            with self.subTest(
                    msg="Response doesn't include the User's password."):
                with self.assertRaises(KeyError):
                    body["password"]  # pylint: disable=pointless-statement


class TestRoutePutRoot(TestCase):
    """Tests for `PUT /user`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        query = """
            INSERT INTO
                hoops_user(handle, full_name, preferred_name, password)
            VALUES
                ('user', 'A Full Name', 'Nickname', '@ new p4s5w0rd')
            RETURNING id;
        """

        async with get_test_client() as clients:
            client, database = clients

            await database.connect()
            result = await database.execute_and_return(query)
            await database.disconnect()

            user_id = result[0]["id"]

            response = await client.put(
                "/user",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"},
                json={"handle": "new_handle"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                msg="Responds with User's updated information."
            ):
                body = response.json()

                with self.subTest():
                    self.assertEqual(body["id"], str(user_id))
                with self.subTest():
                    self.assertEqual(body["handle"], "new_handle")
                with self.subTest():
                    self.assertEqual(body["full_name"], "A Full Name")
                with self.subTest():
                    self.assertEqual(body["preferred_name"],
                                     "Nickname")
                with self.subTest(
                        msg="Response body does not include new password."):
                    self.assertNotIn("password", body.keys())

            with self.subTest(
                    msg="Changes to user show in database."):
                body = response.json()

                await database.connect()
                query_result = await database.execute_and_return(sql.SQL("""
                    SELECT handle FROM hoops_user
                    WHERE id = {user_id};
                """).format(user_id=sql.Literal(user_id)))
                await database.disconnect()

                result = query_result[0]

                with self.subTest(
                        msg="Given handle & database handle match."):
                    self.assertEqual(result["handle"], "new_handle")

    async def test_cant_update_password(self) -> None:
        """PUT /user can't update a User's password."""
        query = """
            INSERT INTO
                hoops_user(handle, full_name, preferred_name, password)
            VALUES
                ('user', 'A Full Name', 'Nickname', '@ new p4s5w0rd')
            RETURNING id;
        """

        async with get_test_client() as clients:
            client, database = clients

            await database.connect()
            result = await database.execute_and_return(query)
            await database.disconnect()

            user_id = result[0]["id"]

            response = await client.put(
                "/user",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"},
                json={"password": "this won't work"})

            with self.subTest(
                    msg="Responds with a status code of 422."):
                self.assertEqual(422, response.status_code)


class TestRoutePutPassword(TestCase):
    """Tests for `PUT /user/password`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        query = """
            INSERT INTO
                hoops_user(handle, full_name, preferred_name, password)
            VALUES
                ('user', 'A Full Name', 'Nickname', '@ new p4s5w0rd')
            RETURNING id;
        """

        async with get_test_client() as clients:
            client, database = clients

            await database.connect()
            result = await database.execute_and_return(query)
            await database.disconnect()

            user_id = result[0]["id"]

            response = await client.put(
                "/user/password",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"},
                json="updated password")

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                msg="Responds with User's information."
            ):
                body = response.json()

                with self.subTest():
                    self.assertEqual(body["id"], str(user_id))
                with self.subTest():
                    self.assertEqual(body["handle"], "user")
                with self.subTest():
                    self.assertEqual(body["full_name"], "A Full Name")
                with self.subTest():
                    self.assertEqual(body["preferred_name"],
                                     "Nickname")
                with self.subTest(
                        msg="Response body does not include new password."):
                    self.assertNotIn("password", body.keys())

            with self.subTest(
                    msg="Changes to user show in database."):
                body = response.json()

                await database.connect()
                query_result = await database.execute_and_return(sql.SQL("""
                    SELECT
                        (password = crypt({password}, password))
                        AS pwmatch
                    FROM hoops_user
                    WHERE
                        id = {user_id};
                """).format(
                    user_id=sql.Literal(user_id),
                    password=sql.Literal("updated password")))
                await database.disconnect()

                result = query_result[0]

                with self.subTest(
                        msg="Database contains updated password."):
                    self.assertTrue(result["pwmatch"])


class TestRouteDeleteRoot(TestCase):
    """Tests for `DELETE /user`."""

    async def test_valid_request(self) -> None:
        """Testing a valid request's response."""
        query = """
            INSERT INTO
                hoops_user(handle, full_name, preferred_name, password)
            VALUES
                ('user', 'A Full Name', 'Nickname', '@ new p4s5w0rd')
            RETURNING id;
        """

        async with get_test_client() as clients:
            client, database = clients

            await database.connect()
            result = await database.execute_and_return(query)
            await database.disconnect()

            user_id = result[0]["id"]

            response = await client.delete(
                "/user",
                headers={
                    **get_token_header(user_id),
                    "accept": "application/json"})

            with self.subTest(
                    msg="Responds with a status code of 200."):
                self.assertEqual(200, response.status_code)

            with self.subTest(
                msg="Responds with deleted User's information."
            ):
                body = response.json()

                with self.subTest():
                    self.assertEqual(body["id"], str(user_id))
                with self.subTest():
                    self.assertEqual(body["handle"], "user")
                with self.subTest():
                    self.assertEqual(body["full_name"], "A Full Name")
                with self.subTest():
                    self.assertEqual(body["preferred_name"],
                                     "Nickname")
                with self.subTest(
                        msg="Response body does not include new password."):
                    self.assertNotIn("password", body.keys())

            with self.subTest(
                    msg="User is removed from database."):
                body = response.json()

                await database.connect()
                query_result = await database.execute_and_return(sql.SQL("""
                    SELECT *
                    FROM hoops_user
                    WHERE id = {user_id};
                """).format(
                    user_id=sql.Literal(user_id)))
                await database.disconnect()

                self.assertEqual(len(query_result), 0)


if __name__ == "__main__":
    main()
