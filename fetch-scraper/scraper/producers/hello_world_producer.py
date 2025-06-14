"""
A HelloWorld producer that produces whatever string it was given

Provided as an example. Useless in production.
"""

import uuid

from .producer import Producer


class HelloWorldProducer(Producer[str]):
    """
    Produces the same string every time
    """

    def __init__(self, msg: str) -> None:
        self.message = msg
        self.unique_id = str(uuid.uuid4())

    def consume(self) -> list[str]:
        return [self.message]

    def serialise(self, target: str) -> bytes:
        return target.encode("utf-8")

    def get_id(self, item: str) -> str:
        return self.unique_id
