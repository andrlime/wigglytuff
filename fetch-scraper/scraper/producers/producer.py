"""
An abstract producer that produces anything of any type
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class Producer(ABC, Generic[T]):
    """
    Abstract producer that produces anything of any type T

    T can be anything, but should be serialisable into bytes
    """

    @abstractmethod
    def consume(self) -> list[T]:
        """
        Abstract method to consume data from some source and return some List[T]
        """
        pass

    @abstractmethod
    def serialise(self, target: T) -> bytes:
        """
        Abstract method to convert some T to bytes
        """
        pass

    @abstractmethod
    def get_id(self, item: T) -> str:
        """
        Returns a unique ID for a given item.

        Ideally does some hashing (or generate a UUID), but can be static for debug producers.
        """
