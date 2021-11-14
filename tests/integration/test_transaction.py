"""Tests API routes under `/transaction`."""
#
# # testing dependencies
# from datetime import datetime, timedelta, timezone
# from decimal import Decimal
# from typing import Any, Dict, List
# import unittest
# from uuid import uuid1, UUID
#
# # test dependencies
# # external
# from db_wrapper import SyncClient, ConnectionParameters
# from db_wrapper.model import sql
# from flask.testing import FlaskClient
# from werkzeug.test import TestResponse
# # internal
# from manage import sync, Config as ManageConfig
# from tests.factories import models as Factory
#
# # app under test
# from hoops import create_app
# from hoops.app import Config as AppConfig
#
# TestCase = unittest.TestCase
#
#
# def clear_test_db(db_client: SyncClient, config: ConnectionParameters) -> None:
#     """Drop all public in given database client."""
#     query = sql.SQL("""
#         DROP SCHEMA public CASCADE;
#         CREATE SCHEMA public;
#         GRANT ALL ON SCHEMA public TO {user};
#         GRANT ALL ON SCHEMA public TO public;
#         COMMENT ON SCHEMA public IS 'standard public schema';
#     """).format(user=sql.Identifier(config.user))
#
#     db_client.connect()
#     db_client.execute(query)
#     db_client.disconnect()
#
#
# def get_test_db() -> SyncClient:
#     """Create database client & return it."""
#     # test database connection data
#     host = 'localhost'
#     port = 9432
#     user = 'test'
#     password = 'pass'
#     database = 'test'
#
#     # create app database client
#     test_db_params = ConnectionParameters(host, port, user, password, database)
#     client = SyncClient(test_db_params)
#
#     # drop any existing test tables
#     clear_test_db(client, test_db_params)
#
#     # rebuild database from app model schema
#     config = ManageConfig(user, password, host, port, database)
#     sync(['noprompt'], config)
#
#     return client
#
#
# def get_test_client(database: SyncClient) -> FlaskClient:
#     """Create an application instance configured for testing."""
#     test_config = AppConfig(
#         database=database,
#         debug=True)
#
#     test_app = create_app(test_config)
#     test_app.testing = True
#
#     return test_app.test_client()
#
#
# class TestRoute(TestCase):
#     """Tests for `/new` route."""
#
#     database: SyncClient
#     client: FlaskClient
#
#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.database = get_test_db()
#         cls.client = get_test_client(cls.database)
#
#
# class TestRouteNewValidRequest(TestRoute):
#     """Test `/new` valid API request."""
#
#     response: TestResponse
#
#     @classmethod
#     def setUpClass(cls) -> None:
#         super().setUpClass()
#
#         cls.response = cls.client.post(
#             '/transaction/new',
#             json={
#                 "amount": "1.00",
#                 "description": "a description",
#                 "payee": "a payee",
#                 "timestamp": "2019-12-10T08:12-05:00"})
#
#     def test_response_is_201(self) -> None:
#         """Responds with status code of 201 Created."""
#         self.assertIn('201', self.response.status)
#
#     def test_response_is_json(self) -> None:
#         """Responds with Content-Type: application/json Header."""
#         content_type: str = ''
#
#         # get Content-Type header
#         for header in self.response.headers:
#             if header[0] == 'Content-Type':
#                 content_type = header[1]
#
#         self.assertEqual(content_type, 'application/json')
#
#     def test_creating_a_new_transaction_returns_the_transaction(self) -> None:
#         """Responds with newly created Transaction."""
#         body: Any = self.response.get_json()
#
#         with self.subTest():
#             # UUID() will throw an error if body["id"] isn't an id
#             self.assertTrue(UUID(body["id"]))
#         with self.subTest():
#             self.assertEqual(body['amount'], "1.00")
#         with self.subTest():
#             self.assertEqual(body['description'], "a description")
#         with self.subTest():
#             self.assertEqual(body['payee'], "a payee")
#         with self.subTest():
#             self.assertEqual(body['timestamp'], "2019-12-10T13:12:00+00:00")
#
#     def test_new_transaction_is_in_database(self) -> None:
#         """New transaction is found in database after processing Request."""
#         body: Any = self.response.get_json()
#         new_id = UUID(body["id"])
#
#         self.database.connect()
#         result = self.database.execute_and_return(sql.SQL("""
#             SELECT * FROM transaction
#             WHERE id = {tran_id};
#             """).format(tran_id=sql.Literal(new_id)))[0]
#         self.database.disconnect()
#
#         with self.subTest():
#             self.assertEqual(result["id"], new_id)
#         with self.subTest():
#             self.assertEqual(result['amount'], Decimal("1.00"))
#         with self.subTest():
#             self.assertEqual(result['description'], "a description")
#         with self.subTest():
#             self.assertEqual(result['payee'], "a payee")
#         with self.subTest():
#             self.assertEqual(result['timestamp'],
#                              datetime.fromisoformat(
#                                  "2019-12-10T13:12:00+00:00"))
#
#
# class TestRouteNewInValidRequest(TestRoute):
#     """Test `/new` invalid API request."""
#
#     @ classmethod
#     def setUpClass(cls) -> None:
#         super().setUpClass()
#
#     def test_request_isnt_json_returns_400(self) -> None:
#         """Responds 400 to POST requests sending non-json data."""
#         response = self.client.post(
#             '/transaction/new',
#             data='invalid data')
#
#         self.assertIn('400', response.status)
#
#     def test_request_isnt_transaction(self) -> None:
#         """
#         Responds 400 to POST requests sending json that isn't a Transaction.
#         """
#         response = self.client.post(
#             '/transaction/new',
#             json={'data': "isn't a transaction"})
#
#         self.assertIn('400', response.status)
#
#
# class TestRouteOneValidRequest(TestRoute):
#     """Test `/one/<id>` valid API request."""
#
#     transaction: Dict[str, Any]
#     response: TestResponse
#
#     @classmethod
#     def setUpClass(cls) -> None:
#         super().setUpClass()
#
#         tran = Factory.TransactionData.create()
#         cls.database.connect()
#         cls.database.execute(sql.SQL("""
#             INSERT INTO transaction(id, amount, description, payee, timestamp)
#             VALUES ({tran_id}, {amount}, {description}, {payee}, {timestamp});
#             """).format(
#             tran_id=sql.Literal(tran.id),
#             amount=sql.Literal(tran.amount),
#             description=sql.Literal(tran.description),
#             payee=sql.Literal(tran.payee),
#             timestamp=sql.Literal(tran.timestamp),
#         ))
#         cls.database.disconnect()
#
#         cls.transaction = tran.dict()
#         cls.response = cls.client.get(f"/transaction/one/{str(tran.id)}")
#
#     def test_response_is_201(self) -> None:
#         """Responds with status code of 200 OK."""
#         self.assertIn('200', self.response.status)
#
#     def test_response_is_json(self) -> None:
#         """Responds with Content-Type: application/json Header."""
#         content_type: str = ''
#
#         # get Content-Type header
#         for header in self.response.headers:
#             if header[0] == 'Content-Type':
#                 content_type = header[1]
#
#         self.assertEqual(content_type, 'application/json')
#
#     def test_responds_with_requested_transaction(self) -> None:
#         """Responds with requested Transaction."""
#         body: Any = self.response.get_json()
#
#         with self.subTest():
#             self.assertEqual(body['id'],
#                              str(self.transaction['id']))
#         with self.subTest():
#             self.assertEqual(body['amount'],
#                              str(self.transaction['amount']))
#         with self.subTest():
#             self.assertEqual(body['description'],
#                              self.transaction['description'])
#         with self.subTest():
#             self.assertEqual(body['payee'],
#                              self.transaction['payee'])
#         with self.subTest():
#             self.assertEqual(body['timestamp'],
#                              self.transaction['timestamp']
#                              .astimezone(timezone.utc)
#                              .isoformat())
#
#
# class TestRouteOneInValidRequest(TestRoute):
#     """Test `/one` invalid API request."""
#
#     @ classmethod
#     def setUpClass(cls) -> None:
#         super().setUpClass()
#
#     def test_request_id_doesnt_exist(self) -> None:
#         """Responds 404 to requests for a transaction that doesn't exist."""
#         response = self.client.get(f'/transaction/one/{uuid1()}')
#
#         self.assertIn('404', response.status)
#
#     def test_request_bad_id(self) -> None:
#         """
#         Responds 400 to requests for a transaction with an invalid id.
#         """
#         response = self.client.get('/transaction/one/not_a_uuid')
#
#         self.assertIn('400', response.status)
#
#
# class TestRouteManyValidRequest(TestRoute):
#     """Test `/many` valid API request."""
#
#     transactions: List[Dict[str, Any]]
#     response: TestResponse
#     first_id: UUID
#     first_ts: datetime
#
#     @classmethod
#     def setUpClass(cls) -> None:
#         super().setUpClass()
#
#         cls.first_ts = datetime.now().astimezone(timezone.utc)
#
#         def _build_tran(num: int) -> Dict[str, Any]:
#             timestamp = cls.first_ts - timedelta(days=num)
#
#             return Factory.TransactionData.create_with_data({
#                 'timestamp': timestamp.isoformat()
#             }).dict()
#
#         trans = [_build_tran(i) for i in range(100)]
#         cls.first_id = trans[0]["id"]
#
#         def _build_row(transaction: Dict[str, Any]) -> sql.Composable:
#             values = [sql.Literal(value) for value in transaction.values()]
#             values_composed = sql.SQL(',').join(values)
#
#             return sql.SQL('({row})').format(row=values_composed)
#
#         rows = [_build_row(tran) for tran in trans]
#         query: sql.Composed = sql.SQL("""
#             INSERT INTO transaction(id, amount, description, payee, timestamp)
#             VALUES {rows};
#             """).format(rows=sql.SQL(',').join(rows))
#
#         cls.database.connect()
#         cls.database.execute(query)
#         cls.database.disconnect()
#
#         cls.transactions = trans
#         cls.response = cls.client.get("/transaction/many")
#
#     def test_response_is_201(self) -> None:
#         """Responds with status code of 200 OK."""
#         self.assertIn('200', self.response.status)
#
#     def test_response_is_json(self) -> None:
#         """Responds with Content-Type: application/json Header."""
#         content_type: str = ''
#
#         # get Content-Type header
#         for header in self.response.headers:
#             if header[0] == 'Content-Type':
#                 content_type = header[1]
#
#         self.assertEqual(content_type, 'application/json')
#
#     def test_responds_with_transactions(self) -> None:
#         """Responds with a list of transactions."""
#         body: Any = self.response.get_json()
#         first_body = body[0]
#         first_tran = self.transactions[0]
#
#         # don't test for full equality with id, only testing that the first
#         # result is a transaction
#         with self.subTest():
#             # UUID() will throw an error if body["id"] isn't an id
#             # self.assertTrue(UUID(first_body["id"]))
#             self.assertEqual(first_body["id"],
#                              str(self.first_id))
#         with self.subTest():
#             self.assertEqual(first_body['amount'],
#                              str(first_tran['amount']))
#         with self.subTest():
#             self.assertEqual(first_body['description'],
#                              first_tran['description'])
#         with self.subTest():
#             self.assertEqual(first_body['payee'],
#                              first_tran['payee'])
#         # don't test for full equality with timestamp, only testing that the
#         # first result is a transaction
#         with self.subTest():
#             # self.assertTrue(datetime.fromisoformat(first_body['timestamp']))
#             self.assertEqual(first_body["timestamp"],
#                              self.first_ts.isoformat())
#
#     def test_response_defaults_to_50_transactions(self) -> None:
#         """Response is 50 items long when no limit is specified."""
#         # limit # of items to limit # of assertions
#         response = self.client.get('/transaction/many?limit=5')
#         body: Any = self.response.get_json()
#
#         self.assertEqual(len(body), 50)
#
#     def test_response_can_be_given_limit(self) -> None:
#         """Response can be limited using query parameter."""
#         response = self.client.get('/transaction/many?limit=10')
#         body: Any = response.get_json()
#
#         self.assertEqual(len(body), 10)
#
#     def test_response_can_be_paginated(self) -> None:
#         """Response can be paginated using limit & start query parameters."""
#         page1 = self.client.get('/transaction/many?limit=10&page=1')
#         page2 = self.client.get('/transaction/many?limit=10&page=2')
#         body1: Any = page1.get_json()
#         body2: Any = page2.get_json()
#
#         for item in body1:
#             with self.subTest():
#                 self.assertNotIn(item, body2)
#
#     def test_response_is_sorted_by_date(self) -> None:
#         """Response sorts Transactions by timestamp with newest first."""
#         body: Any = self.response.get_json()
#
#         for index, tran in enumerate(body):
#             with self.subTest():
#                 if index != 0:
#                     # assert the current one is older than the previous one
#                     # yesterday < today => True
#                     self.assertLess(
#                         tran["timestamp"],
#                         body[index - 1]["timestamp"])
