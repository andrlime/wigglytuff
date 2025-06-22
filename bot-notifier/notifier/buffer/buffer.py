"""
An abstract buffer
"""

from abc import ABC, abstractmethod


class Buffer(ABC):
    """
    Abstract buffer, ideally lock free
    """

    @abstractmethod
    def push(self, val):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def empty(self):
        pass
