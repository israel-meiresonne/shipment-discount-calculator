from abc import ABC, abstractmethod

from module.transactions import TransactionInterface
from module.utils import Helper


class CalculatorInterface(ABC):
    """This interface defines the contract to be Calculator.
        A Calculator has the sole responsibility of calculating the shipping
        cost for a given transaction.

    Usage:
        - To perform the calculation, this interface is used in combination with the
            abstract classes `CalculatorDecorator` and `WrappableCalculator`
            to implement the decorator pattern.
        - This design choice allows combining an 'unlimited' number of
            conditions without coupling them.
        - Each Calculator implements its own requirements to calculate the
            shipping cost and can be combined with other Calculator, thank the
            decorator pattern, to offer complex multi-requirement calculation.
        - This implementation offers a maximum of flexibility, reusability and
            avoids hard coupling between Calculators.
        - Note that with this implementation, the order in which Calculators
            are wrapped is very important.
        - The flexibility offered by the `FacadeInterface` (see ./module/facades)
            combined with the one offered by Calculators allows the module to
            undertake any situation, from a change of input format to new shipment
            calculation requirements.
    """

    def __init__(self, transaction: TransactionInterface) -> None:
        Helper.check_type('transaction', transaction, TransactionInterface)
        self._transaction = transaction

    @abstractmethod
    def calculate(self) -> TransactionInterface:
        pass
