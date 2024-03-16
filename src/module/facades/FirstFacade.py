from module.calculator import (
    FreePackageCalculator,
    LowerPackageCalculator,
    MaxDiscountCalculator,
    ShippingCalculator
)
from module.core import CalculatorInterface
from module.enums import Period, Provider, Size
from module.transactions import TextTransactionConverter
from module.transactions.concrete import Transaction
from module.utils import FileManager, ShippingRates


class FirstFacade:
    _SEPARATOR = ' '
    _EMPTY = 'Ignore'
    _FILE_PROVIDER_RATES = 'module/config/provider_rates.json'

    @classmethod
    def calculate_shipment(
            cls,
            formatteds: list[str],
            separator: str = _SEPARATOR,
            empty: str = _EMPTY) -> list[str]:
        provider_rates = cls._load_provider_rates()
        history = []
        completed_transactions = []
        transactions = cls._formatted_to_transaction(
            formatteds, separator, empty)
        for transaction in transactions:
            calculator = cls.new_calculator(
                transaction, provider_rates, history)
            history.append(transaction)
            try:
                completed_transaction: Transaction = calculator.calculate()
            except Exception:
                pass
            else:
                history.append(completed_transaction)
            finally:
                completed_transactions.append(completed_transaction)
        completed_formatteds = cls._transaction_to_formatted(
            transactions, separator, empty)
        return completed_formatteds

    @classmethod
    def _load_provider_rates(cls) -> ShippingRates:
        json_dict: dict = FileManager.load_json(cls._FILE_PROVIDER_RATES)
        if not isinstance(json_dict, dict):
            raise Exception("Provider rate is not a dictionary")
        return ShippingRates(json_dict)

    @staticmethod
    def _formatted_to_transaction(
            formatteds: list[str],
            separator: str,
            empty: str) -> list[Transaction]:
        transactions = []
        params = {
            'separator': separator,
            'empty': empty,
            'formatted': None,
        }
        for formatted in formatteds:
            params['formatted'] = formatted
            converter = TextTransactionConverter(**params)
            transaction = converter.to_transaction()
            transactions.append(transaction)
        return list(sorted(
            transactions, key=lambda t: t.get_date().get_unix_timestamp()))

    @staticmethod
    def _transaction_to_formatted(
            transactions: list[Transaction],
            separator: str,
            empty: str) -> list[str]:
        formatteds = []
        params = {
            'separator': separator,
            'empty': empty,
            'transaction': None,
        }
        for transaction in transactions:
            params['transaction'] = transaction
            converter = TextTransactionConverter(**params)
            formatted = converter.to_format()
            formatteds.append(formatted)
        return formatteds

    @staticmethod
    def new_calculator(
            transaction: Transaction,
            rates: ShippingRates,
            history: list[Transaction]) -> CalculatorInterface:
        wrappable = ShippingCalculator(transaction, rates)
        wrapper1 = LowerPackageCalculator(wrappable, Size.S, rates)
        params2 = {
            'wrapped': wrapper1,
            'size': Size.L,
            'provider': Provider.LP,
            'position': 3,
            'period': Period.MONTH,
            'history': history
        }
        wrapper2 = FreePackageCalculator(**params2)
        params3 = {
            'wrapped': wrapper2,
            'period': Period.MONTH,
            'max_discount': 10,
            'history': history,
        }
        wrapper3 = MaxDiscountCalculator(**params3)
        return wrapper3
