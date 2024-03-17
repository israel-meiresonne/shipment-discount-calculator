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
        values = [
            transaction.get_date().iso_format(),
            transaction.get_size(),
            transaction.get_provider(),
            str(transaction.get_amount()),
            str(transaction.get_discount())
        ]
        joined = self._separator.join(values)
        formatted = joined.replace(str(None), self._empty)
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
