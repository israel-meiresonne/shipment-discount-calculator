from abc import ABC, abstractmethod

from module.utils import Date


class TransactionInterface(ABC):
    @abstractmethod
    def __init__(self, date: Date) -> None:
        self._date = date
        self._amount = None
        self._discount = None

    def get_date(self) -> Date:
        return self._date

    def set_amount(self, amount: float):
        self._amount = amount

    def set_discount(self, discount: float):
        if self._amount:
            raise Exception(
                f"The amount have to be set first: amount='{self._amount}'"
            )
        if (discount <= 0) or (discount > self._amount):
            detail = f"discount='{discount}', amount='{self._amount}'"
            raise ValueError(
                f"The discount have to be '0 < discount <= amount': {detail}"
            )
        self._discount = discount

    def get_amount(self) -> None | float:
        return self._amount

    def get_discount(self) -> None | float:
        return self._discount

    def __eq__(self, __value: object) -> bool:
        return self.__dict__ == __value.__dict__
