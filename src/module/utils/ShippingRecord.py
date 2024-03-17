from module.enums import Provider, Size


class ShippingRecord:
    _instances = {}

    def __new__(
            cls,
            provider: Provider,
            size: Size,
            price: float) -> 'ShippingRecord':
        gen_hash = cls.generate_hash(provider, size, price)
        if gen_hash not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[gen_hash] = instance
        return cls._instances[gen_hash]

    def __init__(self, provider: Provider, size: Size, price: float):
        self._provider = provider
        self._size = size
        self._price = price

    def get_provider(self) -> Provider:
        return self._provider

    def get_size(self) -> Size:
        return self._size

    def get_price(self) -> float:
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
