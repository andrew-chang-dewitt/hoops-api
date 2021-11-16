"""Tests for common error handling across all routes."""

from uuid import UUID
from unittest import main, IsolatedAsyncioTestCase as TestCase

from db_wrapper.model import sql

# internal test dependencies
from tests.helpers.application import get_test_client


class TestRoutePost(TestCase):
    """Testing HTTP Status Codes returned."""

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
                "/user/",
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


if __name__ == "__main__":
    main()
