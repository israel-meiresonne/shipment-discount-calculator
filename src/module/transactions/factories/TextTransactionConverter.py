from module.enums import Provider, Size
from module.transactions.concrete import Transaction
from module.utils import Date
from . import TransactionConverter


class TextTransactionConverter(TransactionConverter):
    def __init__(
            self,
            separator: str,
            empty: str,
            formatted: str = None,
            transaction: Transaction = None):
        super().__init__(formatted=formatted, transaction=transaction)
        self._separator = separator
        self._empty = empty

    def _create_formatted(self) -> str:
        transaction = self._transaction
        empty = self._empty
        amount = transaction.get_amount()
        discount = transaction.get_discount()
        is_discount_none = discount is None
        final_amount = amount - discount if (not is_discount_none) else amount
        final_discount = f'{discount:.2f}' if not is_discount_none else empty
        values = [
            transaction.get_date().iso_format(),
            transaction.get_size(),
            transaction.get_provider(),
            f'{final_amount:.2f}',
            final_discount
        ]
        formatted = self._separator.join(values)
        return formatted

    def _create_transaction(self) -> Transaction:
        pieces: list[str] = self._formatted.split(self._separator)
        for i in range(len(pieces)):
            match i:
                case 0:
                    date = Date(pieces[i])
                case 1:
                    size = Size(pieces[i])
                case 2:
                    provider = Provider(pieces[i])
        transaction = Transaction(date, provider, size)
        return transaction
