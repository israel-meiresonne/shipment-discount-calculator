import unittest
from unittest.mock import Mock

from module.calculator import ShippingCalculator
from module.enums import Provider, Size
from module.transactions import Transaction
from module.utils import Date, ShippingRates, ShippingRecord


class TestShippingCalculator(unittest.TestCase):
    def setUp(self) -> None:
        provider = Provider.LP
        size = Size.L
        self.mock_transaction = Mock(spec=Transaction)
        self.mock_rates = Mock(spec=ShippingRates)
        self.transaction = Transaction(Date("2024-02-15"), provider, size)
        self.records = [
            ShippingRecord(Provider.LP, Size.L, 5.00),
            ShippingRecord(Provider.MR, Size.M, 10.50)
        ]

    def test_init(self):
        """Test __init__ sets attributes correctly."""
        transaction = self.mock_transaction
        rates = self.mock_rates
        calculator = ShippingCalculator(transaction, rates)
        self.assertEqual(calculator._transaction, transaction)
        self.assertEqual(calculator._rates, rates)

    def test_init_invalid_rate(self):
        """Test __init__ sets attributes correctly."""
        with self.assertRaises(TypeError):
            ShippingCalculator(self.mock_transaction, 'invalid_rates')

    def test_calculate_sets_amount(self):
        """Test calculate sets transaction amount based on shipping rate."""
        provider = Provider.LP
        size = Size.L
        transaction = self.transaction
        rates = self.mock_rates
        rates.get.return_value = self.records[:1]
        calculator = ShippingCalculator(transaction, rates)
        transaction = calculator.calculate()
        self.assertEqual(transaction.get_amount(), 5.00)
        rates.get.assert_called_once_with([provider], [size])

    def test_calculate_no_matching_rate(self):
        """Test calculate no matching rate found."""
        transaction = self.transaction
        rates = self.mock_rates
        rates.get.return_value = records = []
        calculator = ShippingCalculator(transaction, rates)
        with self.assertRaises(AttributeError) as e:
            calculator.calculate()
        self.assertEqual(
            str(e.exception),
            f"No record match: records='{records}'"
        )

    def test_calculate_to_many_matching_rate(self):
        """Test calculate too many rate match."""
        transaction = self.transaction
        records = self.records
        rates = self.mock_rates
        rates.get.return_value = records
        calculator = ShippingCalculator(transaction, rates)
        with self.assertRaises(AttributeError) as e:
            calculator.calculate()
        self.assertEqual(
            str(e.exception),
            f"Too many record match: records='{records}'"
        )
