"""
An abstract producer that produces anything of any type
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class Consumer(ABC, Generic[T]):
    """
    Abstract consumer that consumes anything of any type T

    T can be anything
    """

    @abstractmethod
    def consume(self, message: T) -> list[T]:
        """
        Abstract method to consume data from some source and handle it somehow
        """
        pass
