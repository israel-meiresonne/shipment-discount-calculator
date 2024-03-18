from module.core import CalculatorInterface
from module.transactions import TransactionInterface


class WrappableCalculator(CalculatorInterface):
    def calculate(self) -> TransactionInterface:
        pass
