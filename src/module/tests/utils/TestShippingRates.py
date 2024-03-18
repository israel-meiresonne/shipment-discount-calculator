import unittest
from unittest.mock import patch

from module.utils import ShippingRates, ShippingRecord
from module.enums import Provider, Size


class TestShippingRates(unittest.TestCase):
    def setUp(self) -> None:
        self.rates1 = {
            'LP': {
                'S': 1.5,
                'M': 4.90,
                'L': 6.90
            },
            'MR': {
                'S': 2,
                'M': 3,
                'L': 4
            }
        }
        self.records1 = [
            ShippingRecord(Provider.LP, Size.S, 1.5,),
            ShippingRecord(Provider.LP, Size.M, 4.90),
            ShippingRecord(Provider.LP, Size.L, 6.90),
            ShippingRecord(Provider.MR, Size.S, 2),
            ShippingRecord(Provider.MR, Size.M, 3),
            ShippingRecord(Provider.MR, Size.L, 4),
        ]

    @staticmethod
    def sort_recors(records: list[ShippingRecord]) -> list[ShippingRecord]:
        return sorted(records, key=lambda r: r.get_price())

    @patch('module.enums.Provider')
    @patch('module.enums.Size')
    def test_init_valid_rates(self, mock_size, mock_provider):
        """Test ShippingRates initialization with a valid rates dictionary."""
        rates = self.rates1
        shipping_rates = ShippingRates(rates)
        self.assertEqual(shipping_rates._rates, rates)

    def test_init_invalid_rates_type(self):
        """Test ShippingRates initialization with invalid rates type (not a dict)."""
        with self.assertRaises(TypeError):
            ShippingRates("invalid_rates")

    def test_get_no_filters(self):
        """Test get() with no filters returns all records."""
        rates = self.rates1
        shipping_rates = ShippingRates(rates)
        expected_records = self.records1
        records = shipping_rates.get()
        self.assertEqual(set(records), set(expected_records))

    def test_get_with_provider_filter(self):
        """Test get() with a provider filter."""
        rates = self.rates1
        shipping_rates = ShippingRates(rates)
        expected_records = [
            record for record in self.records1
            if record.get_provider() == Provider.LP]
        records = shipping_rates.get(providers=[Provider.LP])
        self.assertEqual(set(records), set(expected_records))

    def test_get_with_size_filter(self):
        """Test get() with a size filter."""
        rates = self.rates1
        shipping_rates = ShippingRates(rates)
        expected_records = [
            record for record in self.records1
            if record.get_size() == Size.S]
        records = shipping_rates.get(sizes=[Size.S])
        self.assertEqual(set(records), set(expected_records))

    def test_get_with_both_filters(self):
        """Test get() with both provider and size filters."""
        def is_match(
                record: ShippingRecord,
                provider: Provider,
                size: Size) -> bool:
            return record.get_provider() == provider and\
                record.get_size() == size
        rates = self.rates1
        shipping_rates = ShippingRates(rates)
        expected_records = [
            record for record in self.records1
            if is_match(record, Provider.MR, Size.S)
        ]
        records = shipping_rates.get(providers=[Provider.MR], sizes=[Size.S])
        self.assertEqual(set(records), set(expected_records))

    def test_get_missing_rate(self):
        """Test get() with a combination where rate is missing."""
        rates = self.rates1
        del rates[Provider.LP][Size.L]
        shipping_rates = ShippingRates(rates)
        records = shipping_rates.get(providers=[Provider.LP], sizes=[Size.L])
        self.assertEqual(records, [])
