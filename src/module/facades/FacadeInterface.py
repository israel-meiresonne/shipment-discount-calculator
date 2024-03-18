from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class FacadeInterface(ABC):
    """This class plays the role of a Facade between the client's code and the
        whole module.
        It is responsible for providing the client code with access to the
        Calculator which computes the shipping cost.

    Usage:
    - For each new set of calculation rules, a new implementation of this
        interface will be added.
    - To provide shipment calculations, children will rely on a combination of
        Calculator (see ./module/core and ./module/calculator).
    - This implementation allows maximum flexibility by allowing the
        co-existence of a multiple set of calculation rules totally
        independent of each other.
    - The structured data passed to the method `calculate_shipment` is
        not bound to any specific type or format that allows to implement
        the interface for any type or data format encountered.
        For instance, you can implement a facade that handles transactions
        in a JSON format.

    """

    @classmethod
    @abstractmethod
    def calculate_shipment(
            cls,
            iso_country: str,
            formatteds: T) -> T:
        """Calculate the shipment cost

        Args:
            iso_country (str): The 'ISO 3166-1 alpha-2' code of
                a country (i.e.: lt, fr, us,...).
                It represents the country where the transactions occurred.
            formatteds (T): Structured data representing transactions

        Returns:
            T: Structured data containing shipment cost
        """
        pass
