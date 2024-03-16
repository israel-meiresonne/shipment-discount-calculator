from .HelperForCalculator import HelperForCalculator
from module.core import CalculatorDecorator
from module.core.CalculatorInterface import CalculatorInterface
from module.enums import Period, Provider, Size
from module.transactions import Transaction


class FreePackageCalculator(CalculatorDecorator):
    def __init__(
            self,
            wrapped: CalculatorInterface,
            size: Size,
            provider: Provider,
            position: int,
            period: Period,
            history: list[Transaction]):
        super().__init__(wrapped)
        self._size = size
        self._provider = provider
        self._position = position
        self._period = period
        self._history = history

    def _discount(self, transaction: Transaction) -> None:
        filtered = HelperForCalculator.filter_history(
            transaction, self._period, self._history)
        if self.can_discount(filtered):
            amount = transaction.get_amount()
            transaction.set_discount(amount)

    def can_discount(self, filtered: list[Transaction]) -> bool:
        """Check if the discount can be applied

        Args:
            filtered (list[Transaction]): List of filtered transactions

        Returns:
            bool: True if the discount can be applied else False
        """
        size = self._size
        provider = self._provider
        position = self._position
        n = len(filtered)
        i = 0
        count = 0
        while (i < n) and (count < position):
            old_size = filtered[i].get_size()
            old_provider = filtered[i].get_provider()
            if (old_size == size) and (old_provider == provider):
                count += 1
            i += 1
        return count == (position - 1)
