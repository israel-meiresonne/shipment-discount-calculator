from module.calculator import (
    FreePackageCalculator,
    LowerPackageCalculator,
    MaxDiscountCalculator,
    ShippingCalculator
)
from module.core import CalculatorInterface
from module.enums import Period, Provider, Size
from .FacadeInterface import FacadeInterface
from module.transactions import TextTransactionConverter
from module.transactions import Transaction
from module.utils import FileManager, ShippingRates


class FirstFacade(FacadeInterface):
    """<See parent string-doc>

    Steps:
        1. Convert string transactions into Transaction objects.
        2. Sort Transaction objects from older date to the more recent.
        3. Compute each Transaction object with a Calculator.
        4. Convert Transaction objects into their initial format (string).
        5. Merge Computed and Failed string transaction in the same list
        6. Sort the Merged list following the order string transaction
            were input.
        7. Return the sorted list
    """
    _SEPARATOR = ' '
    _EMPTY = '-'
    _FAILED = 'Ignored'
    _FILE_PROVIDER_RATES = 'module/config/provider_rates.json'

    @classmethod
    def calculate_shipment(
            cls,
            iso_country: str,
            formatteds: list[str],
            separator: str = _SEPARATOR,
            empty: str = _EMPTY,
            failed: str = _FAILED) -> list[str]:
        """<See parent string-doc>

        Args:
            iso_country (str): <See parent string-doc>
            formatteds (list[str]): <See parent string-doc>
            separator (str, optional): Separator to split and extract data
                from a transaction.
            empty (str, optional): Placeholder for missing field
            failed (str, optional): Flag appended to transaction to signal malformation

        Returns:
            list[str]: <See parent string-doc>
        """
        provider_rates = cls._retrieve_provider_rates(iso_country)
        history = []
        transactions, failed_formatteds = cls._formatted_to_transaction(
            formatteds,
            separator,
            empty,
            failed
        )
        for transaction in transactions:
            calculator = cls._new_calculator(
                transaction,
                provider_rates,
                history
            )
            completed_transaction: Transaction = calculator.calculate()
            history.append(completed_transaction)
        completed_formatteds = cls._transaction_to_formatted(
            history,
            separator,
            empty
        )
        treated_formatteds = [*completed_formatteds, *failed_formatteds]
        ordered_treated_formatteds = cls._to_initial_order(
            formatteds,
            treated_formatteds
        )
        return ordered_treated_formatteds

    @classmethod
    def _retrieve_provider_rates(cls, country: str) -> ShippingRates:
        """Retrieve pricing rate from a data source (file, database, API, etc...)
            You can inherit and overwrite this method to change the data source

        Args:
            country (str): <See method `calculate_shipment` string-doc>

        Raises:
            TypeError: If the retrieved data is malformed

        Returns:
            ShippingRates: _description_
        """
        json_dict: dict = FileManager.load_json(cls._FILE_PROVIDER_RATES)
        if not isinstance(json_dict, dict):
            raise TypeError("Provider rate is not a dictionary")
        return ShippingRates(json_dict[country])

    @staticmethod
    def _to_initial_order(
            initial_formatteds: list[str],
            treated_formatteds: list[str]) -> list[str]:
        """Sort formatted data in the same order that their where given

        Args:
            initial_formatteds (list[str]): The initial formatted data in the
                order they were given
            treated_formatteds (list[str]): Unordered list of formatted
                data treated

        Raises:
            Exception: If one initial formatted data doesn't exist
                in a list of treated formatted data

        Returns:
            list[str]: Formatted data treated sorted following the order
                of the initial formatted data
        """
        remains = initial_formatteds.copy()
        ordered = []
        while len(remains) > 0:
            for treated_formatted in treated_formatteds:
                if remains[0] in treated_formatted:
                    remains.pop(0)
                    ordered.append(treated_formatted)
                    break
            else:
                raise ValueError(
                    "Can't find initial transaction in among treated " +
                    f"transaction: initial='{remains[0]}'")
        return ordered

    @staticmethod
    def _formatted_to_transaction(
            formatteds: list[str],
            separator: str,
            empty: str,
            failed: str
    ) -> tuple[list[Transaction], list[str]]:
        transactions = []
        failed_formatteds = []
        params = {
            'separator': separator,
            'empty': empty,
            'formatted': None,
        }
        for formatted in formatteds:
            params['formatted'] = formatted
            converter = TextTransactionConverter(**params)
            try:
                transaction = converter.to_transaction()
                transactions.append(transaction)
            except Exception:
                failed_formatted = f'{formatted}{separator}{failed}'
                failed_formatteds.append(failed_formatted)
        sorted_transact = list(sorted(
            transactions,
            key=lambda t: t.get_date().get_unix_timestamp()
        ))
        return sorted_transact, failed_formatteds

    @staticmethod
    def _transaction_to_formatted(
            transactions: list[Transaction],
            separator: str,
            empty: str) -> list[str]:
        formatteds = []
        params = {
            'separator': separator,
            'empty': empty,
            'transaction': None
        }
        for transaction in transactions:
            params['transaction'] = transaction
            converter = TextTransactionConverter(**params)
            formatted = converter.to_format()
            formatteds.append(formatted)
        return formatteds

    @staticmethod
    def _new_calculator(
            transaction: Transaction,
            rates: ShippingRates,
            history: list[Transaction]) -> CalculatorInterface:
        """Generate a calculator that covers all shipping cost
            calculation requirements

        Args:
            transaction (Transaction): The transaction to compute and get its
                shipping cost
            rates (ShippingRates): The pricing rates
            history (list[Transaction]): History of past transactions

        Returns:
            CalculatorInterface: A new Calculator
        """
        # Basic shipment rule:
        #     Apply shipping rates based on provider and size.
        wrappable = ShippingCalculator(transaction, rates)
        # Discount rule 1:
        #     All S shipments should always match the lowest S package
        #     price among the providers.
        wrapper1 = LowerPackageCalculator(
            wrapped=wrappable,
            size=Size.S,
            rates=rates
        )
        # Discount rule 2:
        #     The third L shipment via LP should be free, but only once a
        #     calendar month.
        wrapper2 = FreePackageCalculator(
            wrapped=wrapper1,
            size=Size.L,
            provider=Provider.LP,
            position=3,
            period=Period.MONTH,
            history=history
        )
        # Discount rule 3:
        #     Accumulated discounts cannot exceed 10€ in a calendar month.
        #     If there are not enough funds to fully cover a discount this
        #     calendar month, it should be covered partially.
        wrapper3 = MaxDiscountCalculator(
            wrapped=wrapper2,
            period=Period.MONTH,
            max_discount=10,
            history=history
        )
        return wrapper3
