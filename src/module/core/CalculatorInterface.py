from abc import ABC, abstractmethod

from module.transactions import TransactionInterface
from module.utils import Helper


class CalculatorInterface(ABC):
    def __init__(self, transaction: TransactionInterface) -> None:
        Helper.check_type('transaction', transaction, TransactionInterface)
        self._transaction = transaction

    @abstractmethod
    def calculate(self) -> TransactionInterface:
        pass
