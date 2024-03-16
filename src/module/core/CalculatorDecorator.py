from abc import abstractmethod

from module.core.CalculatorInterface import CalculatorInterface
from module.transactions import TransactionInterface


class CalculatorDecorator(CalculatorInterface):
    def __init__(self, wrapped: CalculatorInterface) -> None:
        super().__init__(wrapped._transaction)
        self._wrapped = wrapped

    def calculate(self) -> TransactionInterface:
        transaction = self._wrapped.calculate()
        self._discount(transaction)
        return transaction

    @abstractmethod
    def _discount(self, transaction: TransactionInterface) -> None:
        pass
