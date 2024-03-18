import unittest

from module.utils import Date
from module.transactions import TransactionInterface


class TestTransactionInterface(unittest.TestCase, TransactionInterface):

    def test_abstract_class_instantiation(self):
        """Test that instantiating the abstract class raises TypeError."""
        with self.assertRaises(TypeError):
            TransactionInterface(Date("2023-03-18"))

    def test_init_valid(self):
        """Test initialization with valid date."""
        test_date = Date("2023-06-15")
        try:
            transaction = MockTransaction(test_date)
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")
        self.assertEqual(transaction._date, test_date)
        self.assertIsNone(transaction._amount)
        self.assertIsNone(transaction._discount)

    def test_init_invalid_date(self):
        """Test initialization with invalid date type."""
        with self.assertRaises(TypeError):
            MockTransaction('test_date')

    def test_get_date(self):
        """Test get_date method to return the initialized date."""
        test_date = Date("2023-02-22")
        transaction = MockTransaction(test_date)
        self.assertEqual(transaction.get_date(), test_date)

    def test_set_amount_valid_float(self):
        """Test set_amount with a valid float amount."""
        transaction = MockTransaction(Date("2023-01-01"))
        transaction.set_amount(100.50)
        self.assertEqual(transaction._amount, 100.50)

    def test_set_amount_valid_int(self):
        """Test set_amount with a valid int amount."""
        transaction = MockTransaction(Date("2023-01-01"))
        transaction.set_amount(100)
        self.assertEqual(transaction._amount, 100)

    def test_set_amount_invalid_type(self):
        """Test set_amount with an invalid type (string)."""
        transaction = MockTransaction(Date("2023-01-01"))
        amount = "invalid_amount"
        with self.assertRaises(TypeError) as e:
            transaction.set_amount(amount)

    def test_set_discount_valid_float(self):
        """Test set_discount with a valid float discount within range."""
        transaction = MockTransaction(Date("2023-01-01"))
        transaction.set_amount(100.00)
        transaction.set_discount(10.50)
        self.assertEqual(transaction._discount, 10.50)

    def test_set_discount_valid_int(self):
        """Test set_discount with a valid int discount within range."""
        transaction = MockTransaction(Date("2023-01-01"))
        transaction.set_amount(100.00)
        transaction.set_discount(10)
        self.assertEqual(transaction._discount, 10)

    def test_set_discount_no_amount_set(self):
        """Test set_discount when amount is not set."""
        transaction = MockTransaction(Date("2023-01-01"))
        with self.assertRaises(Exception) as e:
            transaction.set_discount(10.00)
        self.assertEqual(str(e.exception),
                         "The amount have to be set first: amount='None'")

    def test_set_discount_invalid_range_low(self):
        """Test set_discount with a discount less than 0."""
        transaction = MockTransaction(Date("2023-01-01"))
        transaction.set_amount(100.00)
        with self.assertRaises(ValueError) as e:
            transaction.set_discount(-5.00)
        self.assertEqual(
            str(e.exception),
            "The discount have to be '0 < discount <= amount':" +
            " discount='-5.0', amount='100.0'",
        )

    def test_set_discount_invalid_range_high(self):
        """Test set_discount with a discount greater than amount."""
        transaction = MockTransaction(Date("2023-01-01"))
        transaction.set_amount(100.00)
        with self.assertRaises(ValueError) as e:
            transaction.set_discount(105.00)
        self.assertEqual(
            str(e.exception),
            "The discount have to be '0 < discount <= amount':" +
            " discount='105.0', amount='100.0'",
        )

    def test_get_amount(self):
        """Test get_amount to return the set amount or None."""
        transaction = MockTransaction(Date("2023-05-18"))
        self.assertIsNone(transaction.get_amount())
        transaction.set_amount(250.00)
        self.assertEqual(transaction.get_amount(), 250.00)

    def test_get_discount(self):
        """Test get_discount to return the set discount or None."""
        transaction = MockTransaction(Date("2023-05-18"))
        self.assertIsNone(transaction.get_discount())
        transaction.set_amount(250.00)
        transaction.set_discount(15.75)
        self.assertEqual(transaction.get_discount(), 15.75)

    def test_eq_equal_objects(self):
        """Test __eq__ method for equal objects."""
        date = Date("2023-07-14")
        transaction1 = MockTransaction(date)
        transaction1.set_amount(100.00)
        transaction1.set_discount(10.00)
        transaction2 = MockTransaction(date)
        transaction2.set_amount(100.00)
        transaction2.set_discount(10.00)
        self.assertEqual(transaction1, transaction2)

    def test_eq_different_objects(self):
        """Test __eq__ method for different objects."""
        date = Date("2023-07-14")
        transaction1 = MockTransaction(date)
        transaction1.set_amount(100.00)
        transaction1.set_discount(10.00)
        transaction2 = MockTransaction(date)
        transaction2.set_amount(200.00)
        transaction2.set_discount(5.00)
        self.assertNotEqual(transaction1, transaction2)

    def test_repr(self):
        """Test __repr__ method to return a string representation."""
        date, amount, discount = Date("2023-08-15"), 350.25, 27.80
        transaction = MockTransaction(date)
        transaction.set_amount(amount)
        transaction.set_discount(discount)
        expected_repr = str({
            '_date': date,
            '_amount': amount,
            '_discount': discount
        })
        self.assertEqual(repr(transaction), expected_repr)


class MockTransaction(TransactionInterface):
    def __init__(self, date: Date) -> None:
        super().__init__(date)
