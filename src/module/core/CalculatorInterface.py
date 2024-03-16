from abc import ABC, abstractmethod

from module.transactions import TransactionInterface


class CalculatorInterface(ABC):
    def __init__(self, transaction: TransactionInterface) -> None:
        self._transaction = transaction

    @abstractmethod
    def calculate(self) -> TransactionInterface:
        pass
