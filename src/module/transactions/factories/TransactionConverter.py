from abc import ABC, abstractmethod
from typing import TypeVar

from module.transactions.concrete import Transaction


T = TypeVar("T")


class TransactionConverter(ABC):
    def __init__(self, formatted: T = None, transaction: Transaction = None):
        self._formatted = formatted
        self._transaction = transaction

    def _set_formatted(self, formatted):
        self._formatted = formatted

    def _set_transaction(self, transaction: Transaction):
        self._transaction = transaction

    @abstractmethod
    def create_formatted(self) -> T:
        pass

    @abstractmethod
    def create_transaction(self) -> Transaction:
        pass
