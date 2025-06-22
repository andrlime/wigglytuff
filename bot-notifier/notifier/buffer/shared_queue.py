"""
A shared lock-free queue for consumption by consumers
"""

from .buffer import Buffer

from typing import override
import queue


class SharedQueue(Buffer):
    """
    Queue that can be passed between children that is shared
    """

    def __init__(self):
        self.queue = queue.Queue()

    @override
    def push(self, val):
        self.queue.put(val)

    @override
    def pop(self):
        return self.queue.get()

    @override
    def empty(self):
        lst = []
        while not self.queue.empty():
            lst.append(self.queue.get_nowait())
        return lst
