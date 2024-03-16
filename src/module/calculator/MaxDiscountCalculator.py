from .HelperForCalculator import HelperForCalculator
from module.core import CalculatorDecorator
from module.core.CalculatorInterface import CalculatorInterface
from module.enums import Period
from module.transactions import Transaction


class MaxDiscountCalculator(CalculatorDecorator):
    def __init__(
            self,
            wrapped: CalculatorInterface,
            period: Period,
            max_discount: float,
            history: list[Transaction]):
        super().__init__(wrapped)
        self._period = period
        self._max_discount = max_discount
        self._history = history

    def _discount(self, transaction: Transaction) -> None:
        max_discount = self._max_discount
        filtered = HelperForCalculator.filter_history(
            transaction, self._period, self._history)
        sum_discount = self._aggregate_old_discount(filtered)
        if sum_discount < max_discount:
            amount = transaction.get_amount()
            discount = transaction.get_discount()
            params = {
                'initial_price': amount,
                'period_accumulated': sum_discount,
                'to_apply_discount': discount,
                'max_allowed_discount': max_discount
            }
            new_discount = self._new_discount(**params)
            transaction.set_discount(new_discount)

    def _aggregate_old_discount(self, filtered: list[Transaction]) -> float:
        max_discount = self._max_discount
        n = len(filtered)
        i = 0
        sum_discount = 0
        while (i < n) and (sum_discount < max_discount):
            old_discount = filtered[i].get_discount()
            if isinstance(old_discount, (int, float)):
                sum_discount += old_discount
            i += 1
        return sum_discount

    @staticmethod
    def _new_discount(
            initial_price: float,
            period_accumulated: float,
            to_apply_discount: float,
            max_allowed_discount: float) -> float:
        max_remaining = max_allowed_discount - period_accumulated
        if max_remaining <= 0:
            return 0
        remain_for_next_time = max_remaining - to_apply_discount
        if remain_for_next_time < 0:
            return max_remaining
        elif to_apply_discount > initial_price:
            return initial_price
        else:
            return to_apply_discount
