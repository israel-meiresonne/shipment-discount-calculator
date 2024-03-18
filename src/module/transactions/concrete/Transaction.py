from module.enums import Provider, Size
from module.utils import Date, Helper
from .TransactionInterface import TransactionInterface


class Transaction(TransactionInterface):
    def __init__(
            self,
            date: Date,
            provider: Provider,
            size: Size,
            amount: float = None,
            discount: float = None):
        super().__init__(date, amount, discount)
        Helper.check_type('provider', provider, Provider)
        Helper.check_type('size', size, Size)
        self._provider = provider
        self._size = size

    def get_provider(self) -> Provider:
        return self._provider

    def get_size(self) -> Size:
        return self._size
