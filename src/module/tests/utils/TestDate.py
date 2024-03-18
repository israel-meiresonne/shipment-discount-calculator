import unittest
import datetime

from module.enums import Period
from module.utils import Date


class TestDate(unittest.TestCase, Date):
    SEPARATOR_HYPHEN = '-'

    @staticmethod
    def date_str_to_params(date_str: str, separator: str) -> list[int]:
        date_pieces = date_str.split(separator)
        params = {
            'year': int(date_pieces[0]),
            'month': int(date_pieces[1]),
            'day': int(date_pieces[2]),
        }
        return params

    def test_init_valid_date(self):
        """Test initializing Date object with valid ISO 8601 date."""
        date_str = "2023-03-18"
        test_date = Date(date_str)
        self.assertEqual(test_date._datetime, datetime.datetime.strptime(
            date_str, Date.DATE_FORMAT_ISO_8601))

    def test_init_invalid_date_format(self):
        """Test initializing Date object with invalid date format."""
        date_str = "03-18-2023"  # Not ISO 8601 format
        with self.assertRaises(ValueError):
            Date(date_str)

    def test_init_custom_date_format(self):
        """Test initializing Date object with custom date format."""
        date_str = "18/03/2023"
        custom_format = "%d/%m/%Y"
        test_date = Date(date_str, custom_format)
        self.assertEqual(test_date._datetime,
                         datetime.datetime.strptime(date_str, custom_format))

    def test_year(self):
        """Test year method to get the year of the date."""
        date_str = "2024-02-29"
        test_date = Date(date_str)
        self.assertEqual(test_date.year(), 2024)

    def test_month(self):
        """Test month method to get the month of the date."""
        date_str = "2023-10-31"
        test_date = Date(date_str)
        self.assertEqual(test_date.month(), 10)

    def test_day(self):
        """Test day method to get the day of the date."""
        date_str = "2023-12-25"
        test_date = Date(date_str)
        self.assertEqual(test_date.day(), 25)

    def test_get_unix_timestamp(self):
        """Test get_unix_timestamp method to get the Unix timestamp."""
        date_str = "2023-01-01"
        params1 = self.date_str_to_params(date_str, self.SEPARATOR_HYPHEN)
        expected_timestamp = datetime.datetime(**params1).timestamp()
        test_date = Date(date_str)
        self.assertEqual(test_date.get_unix_timestamp(), expected_timestamp)

    def test_iso_format(self):
        """Test iso_format method to get the date in ISO 8601 format."""
        date_str = "2023-05-12"
        test_date = Date(date_str)
        self.assertEqual(test_date.iso_format(), date_str)

    def test_first_day_invalid_period(self):
        """Test first_day_of method for year period."""
        date_str = "2023-01-01"
        test_date = Date(date_str)
        with self.assertRaises(ValueError):
            test_date.first_day_of('century')

    def test_first_day_of_year(self):
        """Test first_day_of method for year period."""
        date_str = "2023-06-15"
        params1 = self.date_str_to_params("2023-01-01", self.SEPARATOR_HYPHEN)
        expected_timestamp = datetime.datetime(**params1).timestamp()
        test_date = Date(date_str)
        result = test_date.first_day_of(Period.YEAR)
        self.assertEqual(result, expected_timestamp)

    def test_first_day_of_month(self):
        """Test first_day_of method for month period."""
        date_str = "2023-06-15"
        params1 = self.date_str_to_params("2023-06-01", self.SEPARATOR_HYPHEN)
        test_date = Date(date_str)
        expected_timestamp = datetime.datetime(**params1).timestamp()
        result = test_date.first_day_of(Period.MONTH)
        self.assertEqual(result, expected_timestamp)

    def test_first_day_of_day(self):
        """Test first_day_of method for day period."""
        date_str = "2023-06-15"
        params1 = self.date_str_to_params(date_str, self.SEPARATOR_HYPHEN)
        expected_timestamp = datetime.datetime(**params1).timestamp()
        test_date = Date(date_str)
        result = test_date.first_day_of(Period.DAY)
        self.assertEqual(result, expected_timestamp)

    def test_str(self):
        """Test __str__ method to get the string representation of the date."""
        date_str = "2023-02-14"
        test_date = Date(date_str)
        self.assertEqual(str(test_date), str(
            datetime.datetime.strptime(date_str, Date.DATE_FORMAT_ISO_8601)))

    def test_repr(self):
        """Test __repr__ method to get the string representation of the date object."""
        date_str = "2023-02-14"
        test_date = Date(date_str)
        expected_repr = datetime.datetime.strptime(
            date_str, Date.DATE_FORMAT_ISO_8601).__str__()
        self.assertEqual(repr(test_date), expected_repr)
