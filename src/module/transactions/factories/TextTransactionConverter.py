from module.enums import Provider, Size
from module.transactions.concrete import Transaction
from module.utils.other import Date
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

    def create_formatted(self) -> str:
        if self._transaction is None:
            raise Exception("The transaction can't be None")
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
        self._set_formatted(formatted)
        return formatted

    def create_transaction(self) -> Transaction:
        if self._formatted is None:
            raise Exception("The formatted data can't be None")
        pieces: list[str] = self._formatted.split(self._separator)
        for i in range(len(pieces)):
            match i:
                case 0:
                    date = Date(pieces[i])
                case 1:
                    provider = Provider(pieces[i])
                case 2:
                    size = Size(pieces[i])
        transaction = Transaction(date, provider, size)
        self._set_transaction(transaction)
        return transaction
