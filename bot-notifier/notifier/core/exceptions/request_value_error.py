"""
Error class for when a HTTP request value has an error
"""

from notifier.core.exceptions.value_error_wrapper import ValueErrorWrapper


class RequestValueError(ValueErrorWrapper):
    pass
