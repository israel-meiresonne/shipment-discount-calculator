import unittest


from module.enums import Provider, Size
from module.utils import Date
from module.transactions import Transaction


class TestTransaction(unittest.TestCase):

    def test_init_valid(self):
        """Test initialization with valid provider and size."""
        test_date = Date("2023-06-15")
        amount = 12.34
        discount = 5.6
        transaction = Transaction(
            test_date,
            Provider.LP,
            Size.M,
            amount=amount,
            discount=discount
        )
        self.assertEqual(transaction.get_date(), test_date)
        self.assertEqual(transaction.get_provider(), Provider.LP)
        self.assertEqual(transaction.get_size(), Size.M)
        self.assertEqual(transaction.get_amount(), amount)
        self.assertEqual(transaction.get_discount(), discount)

    def test_init_invalid_provider(self):
        """Test initialization with invalid provider type (not a Provider enum)."""
        test_date = Date("2023-02-22")
        with self.assertRaises(TypeError):
            Transaction(test_date, "invalid_provider", Size.L)

    def test_init_invalid_size(self):
        """Test initialization with invalid size type (not a Size enum)."""
        test_date = Date("2023-01-01")
        with self.assertRaises(TypeError):
            Transaction(test_date, Provider.LP, "invalid_size")

    def test_get_provider(self):
        """Test get_provider to return the set provider."""
        transaction = Transaction(Date("2023-05-18"), Provider.MR, Size.S)
        self.assertEqual(transaction.get_provider(), Provider.MR)

    def test_get_size(self):
        """Test get_size to return the set size."""
        transaction = Transaction(
            Date("2023-09-22"), Provider.LP, Size.L)
        self.assertEqual(transaction.get_size(), Size.L)
