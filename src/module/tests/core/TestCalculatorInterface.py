import unittest
from unittest.mock import Mock

from module.core import CalculatorInterface
from module.transactions import TransactionInterface


class TestCalculatorInterface(unittest.TestCase):

    def test_init_sets_transaction(self):
        """Test __init__ sets the transaction attribute."""
        transaction = Mock(spec=TransactionInterface)
        calculator = MockCalculator(transaction)
        self.assertEqual(calculator._transaction, transaction)

    def test_init_invalid_transaction(self):
        """Test __init__ initialize with invalid transaction."""
        with self.assertRaises(TypeError):
            MockCalculator("invalid_transaction")

    def test_init_abstract_class(self):
        """Test __init__ initialization of abstract class."""
        transaction = Mock(spec=TransactionInterface)
        with self.assertRaises(TypeError):
            CalculatorInterface(transaction)


class MockCalculator(CalculatorInterface):
    def calculate(self) -> TransactionInterface:
        pass
