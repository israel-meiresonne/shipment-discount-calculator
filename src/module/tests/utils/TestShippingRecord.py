import unittest

from module.utils import ShippingRecord
from module.enums import Provider, Size


class TestShippingRecord(unittest.TestCase):
    def setUp(self) -> None:
        ShippingRecord._INSTANCES = {}

    def test_init_unique_instance(self):
        """Test ShippingRecord creates a single instance for identical attributes."""
        provider = Provider.LP
        size = Size.M
        price = 10.00
        record1 = ShippingRecord(provider, size, price)
        record2 = ShippingRecord(provider, size, price)
        self.assertIs(record1, record2)
        self.assertEqual(len(ShippingRecord._INSTANCES), 1)

    def test_init_different_instance(self):
        """Test ShippingRecord creates different instances for different attributes."""
        provider1 = Provider.LP
        size1 = Size.M
        price1 = 10.00
        provider2 = Provider.MR
        size2 = Size.S
        price2 = 15.00
        record1 = ShippingRecord(provider1, size1, price1)
        record2 = ShippingRecord(provider2, size2, price2)
        self.assertIsNot(record1, record2)
        self.assertEqual(len(ShippingRecord._INSTANCES), 2)

    def test_init_invalid_provider_type(self):
        """Test initialization with invalid provider type (not a Provider enum)."""
        with self.assertRaises(TypeError):
            ShippingRecord("invalid_provider", Size.M, 10.00)

    def test_init_invalid_size_type(self):
        """Test initialization with invalid size type (not a Size enum)."""
        with self.assertRaises(TypeError):
            ShippingRecord(Provider.LP, "invalid_size", 10.00)

    def test_init_valid_price_int(self):
        """Test initialization with valid int price."""
        record = ShippingRecord(Provider.LP, Size.M, 10)
        self.assertEqual(record.get_price(), 10)

    def test_init_valid_price_float(self):
        """Test initialization with valid float price."""
        record = ShippingRecord(Provider.LP, Size.M, 10.00)
        self.assertEqual(record.get_price(), 10.00)

    def test_get_provider(self):
        """Test get_provider returns the set provider."""
        provider = Provider.MR
        size = Size.L
        price = 20.00
        record = ShippingRecord(provider, size, price)
        self.assertEqual(record.get_provider(), provider)

    def test_get_size(self):
        """Test get_size returns the set size."""
        provider = Provider.LP
        size = Size.S
        price = 5.00
        record = ShippingRecord(provider, size, price)
        self.assertEqual(record.get_size(), size)

    def test_get_price(self):
        """Test get_price returns the set price."""
        provider = Provider.LP
        size = Size.M
        price = 10.00
        record = ShippingRecord(provider, size, price)
        self.assertEqual(record.get_price(), price)

    def test_equality(self):
        """Test object equality based on attributes."""
        provider = Provider.MR
        size = Size.L
        price = 20.00
        record1 = ShippingRecord(provider, size, price)
        record2 = ShippingRecord(provider, size, price)
        self.assertEqual(record1, record2)
        different_record = ShippingRecord(Provider.LP, size, price)
        self.assertNotEqual(record1, different_record)

    def test_hash(self):
        """Test object hash is based on attributes."""
        provider = Provider.MR
        size = Size.L
        price = 20.00
        record1 = ShippingRecord(provider, size, price)
        record2 = ShippingRecord(provider, size, price)
        self.assertEqual(hash(record1), hash(record2))
        different_record = ShippingRecord(Provider.LP, size, price)
        self.assertNotEqual(hash(record1), hash(different_record))

    def test_repr_format(self):
        """Test __repr__ returns a string with expected format."""
        provider = Provider.LP
        size = Size.M
        price = 10.00
        record = ShippingRecord(provider, size, price)
        expected_repr = str({
            '_provider': provider,
            '_size': size,
            '_price': price,
        })
        self.assertEqual(repr(record), expected_repr)
