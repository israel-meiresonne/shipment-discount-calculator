from module.core import WrappableCalculator
from module.transactions import Transaction
from module.utils import ShippingRates


class ShippingCalculator(WrappableCalculator):
    def __init__(self, transaction: Transaction, rates: ShippingRates):
        super().__init__(transaction)
        self._rates = rates

    def calculate(self) -> Transaction:
        rates = self._rates
        transaction: Transaction = self._transaction
        providers = [transaction.get_provider()]
        sizes = [transaction.get_size()]
        record = rates.get(providers, sizes)[0]
        transaction.set_amount(record.get_price())
        return transaction
