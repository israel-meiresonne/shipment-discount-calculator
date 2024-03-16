from module.enums import Provider, Size
from module.utils import Date
from . import TransactionInterface


class Transaction(TransactionInterface):
    def __init__(self, date: Date, provider: Provider, size: Size):
        super().__init__(date)
        self._provider = provider
        self._size = size

    def get_provider(self) -> Provider:
        return self._provider

    def get_size(self) -> Size:
        return self._size
