"""Tests for hoops.transaction."""

# testing dependencies
import unittest
from uuid import uuid1, UUID

# internal dependencies
from hoops.models import (
    Transaction as Model,
    TransactionData as Data,
)

# test helpers
# pylint thinks test is a standard import
# pylint: disable=wrong-import-order
from test.unit import factories
from test.unit.helpers import mock_client, mock_model

# module under test
from hoops.core import transactions as trn

client = mock_client()


class TestTransaction(unittest.TestCase):
    """Tests for core.transactions functions."""

    model: Model

    def setUp(self) -> None:
        self.model = mock_model(Model(client))

    def test_create_one(self) -> None:
        """
        Returns data validated as TransactionData & the create.one on model.
        """
        in_data = factories.models.TransactionData.as_dict()
        result_data, result_method = trn.create_one(in_data, self.model)

        with self.subTest():
            self.assertIsInstance(result_data, Data)
        with self.subTest():
            self.assertIs(result_method, self.model.create.one)

    def test_read_one(self) -> None:
        """Returns id validated as UUID & the read.one_by_id on model."""
        in_data = str(uuid1())
        result_data, result_method = trn.read_one(in_data, self.model)

        with self.subTest():
            self.assertIsInstance(result_data, UUID)
        with self.subTest():
            self.assertIs(result_method, self.model.read.one_by_id)

    def test_read_many(self) -> None:
        """
        Returns None as the default limit & the read.many method on model.
        """
        in_data = None
        result_data, result_method = trn.read_many(in_data, self.model)

        with self.subTest():
            self.assertIsNone(result_data)
        with self.subTest():
            self.assertIs(result_method, self.model.read.many)

    def test_read_many_limit(self) -> None:
        """Can take an int limit on the number of records returned."""
        in_data = 50
        result_data, _ = trn.read_many(in_data, self.model)

        with self.subTest():
            self.assertEqual(result_data, 50)

    def test_read_many_limit_str(self) -> None:
        """Can take an str limit on the number of records returned."""
        in_data = '50'
        result_data, _ = trn.read_many(in_data, self.model)

        with self.subTest():
            self.assertEqual(result_data, 50)

    def test_read_many_limit_str_must_be_int(self) -> None:
        """That str must be convertable to an int."""
        in_data = 'not an int'

        with self.assertRaises(ValueError) as raised:
            trn.read_many(in_data, self.model)

        self.assertIn("invalid literal for int", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
