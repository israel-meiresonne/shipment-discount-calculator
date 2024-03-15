from abc import ABC

from module.utils.other import Date


class TransactionInterface(ABC):
    def __init__(self, date: Date) -> None:
        self._date = date

    def get_date(self) -> Date:
        return self._date
