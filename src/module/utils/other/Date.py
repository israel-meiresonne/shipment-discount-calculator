import datetime


class Date:
    """A class to represent a date using a Unix timestamp."""

    DATE_FORMAT_ISO_8601 = '%Y-%m-%d'

    def __init__(self, date: str, date_format: str = DATE_FORMAT_ISO_8601):
        """
        Args:
            date (float): The date in ISO 8601 format (YYYY-MM-DD).
            date_format (str, optional): The date format. Defaults to
            ISO 8601 format (YYYY-MM-DD).
        """
        self._datetime = datetime.datetime.strptime(date, format)

    def year(self) -> int:
        """
        Returns the year of the date.

        Returns:
            int: The year of the date.
        """
        return self._datetime.year

    def month(self) -> int:
        """
        Returns the month of the date (1-12).

        Returns:
            int: The month of the date.
        """
        return self._datetime.month

    def day(self) -> int:
        """
        Returns the day of the date (1-31).

        Returns:
            int: The day of the date.
        """
        return self._datetime.day

    def get_unix_timestamp(self) -> float:
        """
        Returns the Unix timestamp representing the date.

        Returns:
            float: The date as Unix timestamp.
        """
        return self._datetime.timestamp()

    def iso_format(self) -> str:
        """
        Returns the date in ISO 8601 format (YYYY-MM-DD).

        Returns:
            str: The date in ISO 8601 format.
        """
        return self._datetime.strftime(self.DATE_FORMAT_ISO_8601)

    def first_day_of_month(self) -> int:
        """
        Returns the Unix timestamp of the first day of the month.

        Returns:
            int: The Unix timestamp of the first day of the month.
        """
        return datetime.datetime(self.year(), self.month(), 1).timestamp()

    def last_day_of_month(self) -> int:
        """
        Returns the Unix timestamp of the last day of the month.

        Returns:
            int: The Unix timestamp of the last day of the month.
        """
        next_month = datetime.datetime(self.year(), self.month() + 1, 1)
        return (next_month - datetime.timedelta(days=1)).timestamp()
