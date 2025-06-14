"""
Error class for when a HTTP request value has an error
"""

from scraper.core.exceptions.value_error_wrapper import ValueErrorWrapper


class RequestValueError(ValueErrorWrapper):
    pass
