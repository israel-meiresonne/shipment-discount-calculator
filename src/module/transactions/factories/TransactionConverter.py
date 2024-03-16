from abc import ABC, abstractmethod
from typing import TypeVar

from module.transactions.concrete import Transaction


T = TypeVar("T")


class TransactionConverter(ABC):
    def __init__(self, formatted: T = None, transaction: Transaction = None):
        self._formatted = formatted
        self._transaction = transaction

    def to_format(self) -> T:
        if self._transaction is None:
            raise Exception("The transaction have to be set first")
        formatted = self._formatted
        if formatted is None:
            formatted = self._create_formatted()
            self._formatted = formatted
        return formatted

    def to_transaction(self) -> Transaction:
        if self._formatted is None:
            raise Exception("The formatted data have to be set first")
        transaction = self._transaction
        if transaction is None:
            transaction = self._create_transaction()
            self._transaction = transaction
        return transaction

    @abstractmethod
    def _create_formatted(self) -> T:
        pass

    @abstractmethod
    def _create_transaction(self) -> Transaction:
        pass
