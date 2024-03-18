from module.core import WrappableCalculator
from module.transactions import Transaction
from module.utils import Helper, ShippingRates


class ShippingCalculator(WrappableCalculator):
    def __init__(self, transaction: Transaction, rates: ShippingRates):
        super().__init__(transaction)
        Helper.check_type('rates', rates, ShippingRates)
        self._rates = rates

    def calculate(self) -> Transaction:
        rates = self._rates
        transaction: Transaction = self._transaction
        providers = [transaction.get_provider()]
        sizes = [transaction.get_size()]
        records = rates.get(providers, sizes)
        n_record = len(records)
        if n_record == 0:
            raise AttributeError(f"No record match: records='{records}'")
        if n_record > 1:
            raise AttributeError(f"Too many record match: records='{records}'")
        transaction.set_amount(records[0].get_price())
        return transaction
