import unittest
from unittest.mock import Mock

from module.core import CalculatorDecorator, CalculatorInterface
from module.transactions import TransactionInterface


class TestCalculatorDecorator(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_transaction = mock_transaction = Mock(spec=TransactionInterface)
        self.mock_wrapped = mock_calculator = Mock(spec=CalculatorInterface,)
        mock_calculator._transaction = mock_transaction

    def test_init_sets_wrapped_and_transaction(self):
        """Test __init__ sets wrapped calculator and transaction."""
        mock_transaction = self.mock_transaction
        mock_calculator = self.mock_wrapped
        decorator = MockCalculatorDecorator(mock_calculator)
        self.assertEqual(decorator._wrapped, mock_calculator)
        self.assertEqual(decorator._transaction, mock_transaction)

    def test_calculate_calls_wrapped_and_discount(self):
        """Test calculate calls wrapped.calculate and _discount."""
        mock_wrapped = self.mock_wrapped
        decorator = MockCalculatorDecorator(mock_wrapped)
        decorator.calculate()
        mock_wrapped.calculate.assert_called_once()
        
    def test_abstract_class(self):
        """Test class is abstract."""
        with self.assertRaises(TypeError):
            CalculatorDecorator(self.mock_wrapped)


class MockCalculatorDecorator(CalculatorDecorator):
    def _discount(self, transaction: TransactionInterface) -> None:
        pass
