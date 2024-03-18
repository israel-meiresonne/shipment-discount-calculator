from module.enums import Provider, Size
from .ShippingRecord import ShippingRecord
from .Helper import Helper


class ShippingRates:
    _PROVIDERS = ()
    _SIZES = ()

    def __init__(self, rates: dict) -> None:
        Helper.check_type('rates', rates, dict)
        self._rates = rates
        if len(self._PROVIDERS) == 0:
            self._PROVIDERS = tuple(Provider.__members__.values())
        if len(self._SIZES) == 0:
            self._SIZES = tuple(Size.__members__.values())

    def get(
            self,
            providers: list[Provider] = (),
            sizes: list[Size] = ()) -> list[ShippingRecord]:
        rates = self._rates
        if len(providers) == 0:
            providers = self._PROVIDERS
        if len(sizes) == 0:
            sizes = self._SIZES
        records = set()
        for provider in providers:
            for size in sizes:
                keys = (provider, size)
                price = Helper._recursive_get(rates, keys)
                if price is not  None:
                    record = ShippingRecord(*keys, price)
                    records.add(record)
        return list(records)
