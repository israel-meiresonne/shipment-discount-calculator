from module.enums import Provider, Size
from .Helper import Helper


class ShippingRecord:
    _INSTANCES = {}

    def __new__(
            cls,
            provider: Provider,
            size: Size,
            price: float) -> 'ShippingRecord':
        gen_hash = cls.generate_hash(provider, size, price)
        if gen_hash not in cls._INSTANCES:
            instance = super().__new__(cls)
            cls._INSTANCES[gen_hash] = instance
        return cls._INSTANCES[gen_hash]

    def __init__(self, provider: Provider, size: Size, price: int | float):
        Helper.check_type('provider', provider, Provider)
        Helper.check_type('size', size, Size)
        Helper.check_type('price', price, (int, float))
        self._provider = provider
        self._size = size
        self._price = price

    def get_provider(self) -> Provider:
        return self._provider

    def get_size(self) -> Size:
        return self._size

    def get_price(self) -> int | float:
        return self._price

    @staticmethod
    def generate_hash(provider: Provider, size: Size, price: float) -> int:
        return hash((provider, size, str(price)))

    def __eq__(self, __value: object) -> bool:
        return self.__dict__ == __value.__dict__

    def __hash__(self) -> int:
        return self.generate_hash(self._provider, self._size, self._price)

    def __repr__(self) -> str:
        return str(self.__dict__)
