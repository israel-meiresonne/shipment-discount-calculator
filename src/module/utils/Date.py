import datetime

from module.enums import Period


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
        self._datetime = datetime.datetime.strptime(date, date_format)

    def year(self) -> int:
        """
        To get the year of the date.

        Returns:
            int: The year of the date.
        """
        return self._datetime.year

    def month(self) -> int:
        """
        To get the month of the date (1-12).

        Returns:
            int: The month of the date.
        """
        return self._datetime.month

    def day(self) -> int:
        """
        To get the day of the date (1-31).

        Returns:
            int: The day of the date.
        """
        return self._datetime.day

    def get_unix_timestamp(self) -> float:
        """
        To get the Unix timestamp representing the date.

        Returns:
            float: The date as Unix timestamp.
        """
        return self._datetime.timestamp()

    def iso_format(self) -> str:
        """
        To get the date in ISO 8601 format (YYYY-MM-DD).

        Returns:
            str: The date in ISO 8601 format.
        """
        return self._datetime.strftime(self.DATE_FORMAT_ISO_8601)

    def first_day_of(self, period: Period) -> float:
        """
        To get the first day of the period surrounding the date

        Args:
            period (Period): Period to get the last day of

        Returns:
            float: The Unix timestamp of last day of the period.
        """
        match period:
            case Period.YEAR:
                params = (self.year(), 1, 1)
            case Period.MONTH:
                params = (self.year(), self.month(), 1)
            case Period.DAY:
                params = (self.year(), self.month(), self.day())
            case _:
                raise ValueError(
                    f"This Period is not supported: period='{period}'"
                )
        return datetime.datetime(*params).timestamp()

    def last_day_of(self, period: Period) -> float:
        """
        To get the last day of the period surrounding the date

        Args:
            period (Period): Period to get the last day of

        Returns:
            float: The Unix timestamp of last day of the period.
        """
        match period:
            case Period.YEAR:
                params = (self.year() + 1, 1, 1)
            case Period.MONTH:
                params = (self.year(), self.month() + 1, 1)
            case Period.DAY:
                params = (self.year(), self.month(), self.day() + 1)
            case _:
                raise ValueError(
                    f"This Period is not supported: period='{period}'"
                )
        next_month = datetime.datetime(*params)
        return (next_month - datetime.timedelta(days=1)).timestamp()

    def duration_of(self, period: Period) -> float:
        """
        To get the duration of the period surrounding the date

        Args:
            period (Period): Period surrounding the date

        Returns:
            float: The Unix timestamp of the last day of the month.
        """
        first_day_timestamp = self.first_day_of(period)
        last_day_timestamp = self.last_day_of(period)
        day_duration = datetime.timedelta(
            hours=23, minutes=59, seconds=59, microseconds=59)
        return last_day_timestamp + day_duration - first_day_timestamp

    def __str__(self) -> str:
        return self._datetime.__str__()

    def __repr__(self) -> str:
        return self.__str__()
