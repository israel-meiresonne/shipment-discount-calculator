from module.enums import Period
from module.transactions.concrete import Transaction


class HelperForCalculator:
    @staticmethod
    def filter_history(
            transaction: Transaction,
            period: Period,
            history: list[Transaction]) -> list[Transaction]:
        """Filter list of transactions
        Filter conditions:
            - Retain transactions made between the first day of the period
              surrounding the current transaction and the day the current
              transaction was made.
              In short, Period.date <= history[:].date <= transaction.date
            - Exclude the current transaction from the history.

      Args:
          transaction (Transaction): The current transaction
          period (Period): Period surrounding the current transaction's
              execution date
          history (list[Transaction]): List of transactions to filter

        Returns:
            list[Transaction]: List of filtered transactions
        """
        def filter_history(t: Transaction) -> bool:
            t_time = t.get_date().get_unix_timestamp()
            are_not_same = id(t) != id(transaction)
            return are_not_same and \
                period_start_time <= t_time <= transaction_time
        if len(history) == 0:
            return []
        transaction_date = transaction.get_date()
        period_start_time = transaction_date.first_day_of(period)
        transaction_time = transaction_date.get_unix_timestamp()
        transaction.get_date().get_unix_timestamp()
        filtered = list(filter(filter_history, history))
        return filtered
