"""Tests for common error handling across all routes."""

from unittest import main, IsolatedAsyncioTestCase as TestCase

# external test dependencies
from db_wrapper.model.base import NoResultFound
from pydantic import BaseModel  # pylint: disable=no-name-in-module
# internal test dependencies
from tests.helpers.application import get_test_app, get_test_client


class TestErrorCodes(TestCase):
    """Testing HTTP Status Codes returned."""

    async def test_request_bad_content_type_returns_415(self) -> None:
        """Responds 415 to POST requests with incorrect Content-Type."""
        async with get_test_client(
            get_test_app([('post', '/', lambda: 'a response')])
        ) as clients:
            client, _ = clients

            response = await client.post(
                '/',
                headers={'content-type': 'text/plain'},
                content='invalid data')

        self.assertEqual(415, response.status_code)

    async def test_request_isnt_transaction(self) -> None:
        """
        Responds 422 POST requests sending json that isn't the expected type.
        """
        class BodyType(BaseModel):
            field: int

        def test_handler(body_arg: BodyType) -> BodyType:
            return body_arg

        async with get_test_client(
                get_test_app([('post', '/', test_handler)])
        ) as clients:
            client, _ = clients

            response = await client.post(
                '/',
                json={'data': "isn't a transaction"})

        self.assertEqual(422, response.status_code)

    async def test_no_result_in_database(self) -> None:
        """Responds 404 when no result is found for DB query."""
        async def raise_no_result() -> None:
            raise NoResultFound()

        async with get_test_client(
                get_test_app([('get', '/', raise_no_result)])
        ) as clients:
            client, _ = clients
            response = await client.get('/')

        self.assertEqual(404, response.status_code)


if __name__ == "__main__":
    main()
