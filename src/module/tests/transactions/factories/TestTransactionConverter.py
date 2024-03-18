import unittest
from unittest.mock import patch


from module.transactions import TransactionConverter, Transaction
from typing import TypeVar


T = TypeVar("T")


class TestTransactionConverter(unittest.TestCase):

    def test_to_format_no_transaction(self):
        """Test to_format raises exception with no transaction set."""
        converter = MockTransactionConverter()
        with self.assertRaises(Exception) as e:
            converter.to_format()
        self.assertEqual(str(e.exception),
                         "The transaction have to be set first")

    @patch('module.transactions.concrete.Transaction')
    def test_to_format_with_transaction(self, mock_transaction):
        """Test to_format returns formatted data after calling _create_formatted."""
        converter = MockTransactionConverter(transaction=mock_transaction())
        formatted_data = converter.to_format()
        self.assertIsInstance(formatted_data, type(converter._formatted))

    def test_to_transaction_no_formatted_data(self):
        """Test to_transaction raises exception with no formatted data set."""
        converter = MockTransactionConverter()
        with self.assertRaises(Exception) as e:
            converter.to_transaction()
        self.assertEqual(str(e.exception), "The formatted data have to be set first")

    def test_to_transaction_with_formatted_data(self):
        """Test to_transaction returns transaction after calling 
        _create_transaction."""
        converter = MockTransactionConverter(formatted=T)
        transaction = converter.to_transaction()
        self.assertIsInstance(transaction, Transaction)

    def test_abstract_methods(self):
        """Test _create_formatted and _create_transaction are abstract."""
        with self.assertRaises(TypeError):
            TransactionConverter()  # Cannot instantiate abstract class


class MockTransactionConverter(TransactionConverter):

    def _create_formatted(self) -> T:
        return T

    def _create_transaction(self) -> Transaction:
        return Transaction.__new__(Transaction)
