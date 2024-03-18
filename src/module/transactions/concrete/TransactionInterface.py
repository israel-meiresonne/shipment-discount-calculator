from abc import ABC, abstractmethod

from module.utils import Date, Helper


class TransactionInterface(ABC):
    @abstractmethod
    def __init__(
            self,
            date: Date,
            amount: float = None,
            discount: float = None) -> None:
        Helper.check_type('date', date, Date)
        self._date = date
        self._amount = None
        self._discount = None
        self.set_amount(amount) if amount is not None else None
        self.set_discount(discount) if discount is not None else None

    def get_date(self) -> Date:
        return self._date

    def set_amount(self, amount: int | float):
        Helper.check_type('amount', amount, (int, float))
        self._amount = amount

    def set_discount(self, discount: int | float):
        if self._amount is None:
            raise Exception(
                f"The amount have to be set first: amount='{self._amount}'"
            )
        Helper.check_type('discount', discount, (int, float))
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

    def __repr__(self) -> str:
        return str(self.__dict__)
