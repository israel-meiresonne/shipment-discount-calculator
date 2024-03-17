from module.core import CalculatorDecorator
from module.core.CalculatorInterface import CalculatorInterface
from module.enums import Provider, Size
from module.transactions import Transaction
from module.utils import ShippingRates


class LowerPackageCalculator(CalculatorDecorator):
    def __init__(
            self,
            wrapped: CalculatorInterface,
            size: Size,
            rates: ShippingRates):
        super().__init__(wrapped)
        self._size = size
        self._rates = rates

    def _discount(self, transaction: Transaction) -> None:
        calculator_size = self._size
        transaction_size = transaction.get_size()
        if transaction_size != calculator_size:
            return None
        rates = self._rates
        providers = tuple(Provider.__members__.values())
        records = rates.get(providers, [calculator_size])
        sorted_records = list(sorted(records, key=lambda r: r.get_price()))
        lower_price_record = sorted_records[0]
        lower_price = lower_price_record.get_price()
        initial_amount = transaction.get_amount()
        new_amount = min(initial_amount, lower_price)
        discount = initial_amount - new_amount
        # At this point, discount is '0 <= discount <= initial_amount'
        transaction.set_discount(discount) if discount != 0 else None
