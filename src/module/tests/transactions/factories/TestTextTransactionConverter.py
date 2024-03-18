import unittest
from unittest.mock import patch

from module.transactions import TextTransactionConverter, Transaction
from module.enums import Provider, Size
from module.utils import Date


class TestTextTransactionConverter(unittest.TestCase):
    SEPARATOR = ' '
    EMPTY = '-'

    def test_valid_init_with_transaction(self):
        """Test TextTransactionConverter valid initialization with transaction."""
        transaction = Transaction(
            Date("2024-03-19"),
            Provider.LP,
            Size.M
        )
        converter = TextTransactionConverter(
            separator=self.SEPARATOR,
            empty=self.EMPTY,
            transaction=transaction
        )
        self.assertEqual(converter._separator, self.SEPARATOR)
        self.assertEqual(converter._empty, self.EMPTY)
        self.assertEqual(converter._transaction, transaction)

    def test_valid_init_with_formatted(self):
        """Test TextTransactionConverter valid initialization with formatted data."""
        formatted = self.SEPARATOR.join([
            '2024-03-19',
            'M',
            'LP'
        ])
        converter = TextTransactionConverter(
            separator=self.SEPARATOR,
            empty=self.EMPTY,
            formatted=formatted
        )
        self.assertEqual(converter._separator, self.SEPARATOR)
        self.assertEqual(converter._empty, self.EMPTY)
        self.assertEqual(converter._formatted, formatted)

    # Test cases for _create_formatted

    def test_create_formatted_no_discount(self):
        """Test _create_formatted with a transaction having no discount."""
        transaction = Transaction(
            Date("2024-03-19"),
            Provider.LP,
            Size.M
        )
        transaction.set_amount(amount=100.)
        converter = TextTransactionConverter(
            separator=self.SEPARATOR,
            empty=self.EMPTY,
            transaction=transaction
        )
        formatted_data = converter._create_formatted()
        expected_data = self.SEPARATOR.join([
            '2024-03-19',
            'M',
            'LP',
            '100.00',
            self.EMPTY
        ])
        self.assertEqual(formatted_data, expected_data)

    @patch('module.transactions.concrete.Transaction')
    def test_create_formatted_with_discount(self, mock_transaction):
        """Test _create_formatted with a transaction having a discount."""
        separator = self.SEPARATOR
        transaction = Transaction(
            Date("2024-03-19"),
            Provider.MR,
            Size.S,
            amount=100.,
            discount=5.25
        )
        converter = TextTransactionConverter(
            separator=separator,
            empty=self.EMPTY,
            transaction=transaction
        )
        formatted_data = converter._create_formatted()
        expected_data = separator.join([
            '2024-03-19',
            'S',
            'MR',
            '94.75',
            '5.25'
        ])
        self.assertEqual(formatted_data, expected_data)

    # Test cases for _create_transaction

    def test_create_transaction_valid_data(self):
        """Test _create_transaction with valid formatted data."""
        separator = self.SEPARATOR
        formatted_data = separator.join([
            '2023-10-26',
            'L',
            'LP'
        ])
        converter = TextTransactionConverter(
            separator=separator,
            empty=self.EMPTY,
            formatted=formatted_data
        )
        transaction = converter._create_transaction()
        self.assertEqual(transaction.get_date(), Date("2023-10-26"))
        self.assertEqual(transaction.get_size(), Size.L)
        self.assertEqual(transaction.get_provider(), Provider.LP)
        self.assertIsNone(transaction.get_amount())
        self.assertIsNone(transaction.get_discount())

    def test_create_transaction_invalid_date_format(self):
        """Test _create_transaction with invalid date format in data."""
        separator = self.SEPARATOR
        formatted_data = separator.join([
            'invalid_date',
            'L',
            'LP',
            '250.00',
            '10.00'
        ])
        converter = TextTransactionConverter(
            separator=separator,
            empty=self.EMPTY,
            formatted=formatted_data
        )
        with self.assertRaises(ValueError):
            converter._create_transaction()

    def test_create_transaction_invalid_enum_value(self):
        """Test _create_transaction with invalid enum value in data."""
        separator = self.SEPARATOR
        formatted_data = separator.join([
            '2023-10-26',
            'INVALID_SIZE',
            'LP',
            '250.00',
            '10.00'
        ])
        converter = TextTransactionConverter(
            separator=separator,
            empty=self.EMPTY,
            formatted=formatted_data
        )
        with self.assertRaises(ValueError):
            converter._create_transaction()

    def test_create_transaction_missing_value(self):
        """Test _create_transaction with missing value in data."""
        formatted_data = self.SEPARATOR.join([
            '2023-10-26',
            'L',
            '',  # Missing provider value
        ])
        converter = TextTransactionConverter(
            separator=self.SEPARATOR,
            empty=self.EMPTY,
            formatted=formatted_data
        )
        with self.assertRaises(ValueError):
            converter._create_transaction()
