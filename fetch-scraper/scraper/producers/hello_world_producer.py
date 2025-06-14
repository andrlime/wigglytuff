"""
A HelloWorld producer that produces whatever string it was given
"""

from .producer import Producer


class HelloWorldProducer(Producer[str]):
    def __init__(self, msg: str) -> "HelloWorldProducer":
        self.message = msg

    def consume(self) -> list[str]:
        return self.message

    def serialise(self, target: str) -> bytes:
        return target.encode("utf-8")
