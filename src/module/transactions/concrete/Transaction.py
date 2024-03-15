from module.enums import Provider, Size
from module.utils.other import Date
from . import TransactionInterface


class Transaction(TransactionInterface):
    def __init__(self, date: Date, provider: Provider, size: Size):
        super().__init__(date)
        self._provider = provider
        self._size = size
        self._amount = None
        self._discount = None

    def set_amount(self, amount: float):
        self._amount = amount

    def set_discount(self, discount: float):
        if self._amount:
            raise Exception(
                f"The amount must be set first: amount={self._amount}"
            )
        if (discount < 0) or (discount > self._amount):
            detail = f"discount={discount}, amount={self._amount}"
            raise ValueError(
                f"The discount must be positive and bellow or equal \
                    to the amount: {detail}"
            )
        self._discount = discount

    def get_provider(self) -> Provider:
        return self._provider

    def get_size(self) -> Size:
        return self._size

    def get_amount(self) -> None | float:
        return self._amount

    def get_discount(self) -> None | float:
        return self._discount
