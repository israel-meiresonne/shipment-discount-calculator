from module.enums import Provider, Size
from .ShippingRecord import ShippingRecord


class ShippingRates:
    def __init__(self, rates: dict) -> None:
        self._rates = rates

    def get(
            self,
            providers: list[Provider] = [],
            sizes: list[Size] = []) -> list[ShippingRecord]:
        rates = self._rates
        records = set()
        for provider in providers:
            for size in sizes:
                keys = (provider, size)
                price = self._recursive_get(rates, keys)
                record = ShippingRecord(*keys, price)
                records.add(record)
        return list(records)

    @classmethod
    def _recursive_get(cls, data, keys):
        """
        Recursively retrieves a value from a nested dictionary using
        a list of keys.

        Args:
            data: The nested dictionary to search.
            keys: A list of keys representing the path to the desired value.

        Returns:
            The value found at the specified path within the nested dictionary,
            or None if the path doesn't exist.
        """
        if not keys:
            return data
        key = keys[0]
        if cls.is_iterable(data) and (key in data):
            return cls._recursive_get(data[key], keys[1:])
        else:
            return None

    @staticmethod
    def is_iterable(obj) -> bool:
        """
        Checks if a value is iterable using isinstance().

        Args:
            obj: The value to check.

        Returns:
            True if the value is iterable, False otherwise.
        """
        return isinstance(obj, (str, list, tuple, set, dict)) \
            or hasattr(obj, '__iter__')
