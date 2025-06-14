"""
A wrapper of ValueError

TODO: remove it unless it does something special like logging
"""


class ValueErrorWrapper(ValueError):
    def __init__(self, s: str) -> None:
        super().__init__(s)
