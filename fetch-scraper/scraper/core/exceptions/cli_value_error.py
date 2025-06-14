"""
Error class for when a CLI contains invalid input
"""

from scraper.core.exceptions.value_error_wrapper import ValueErrorWrapper


class CLIValueError(ValueErrorWrapper):
    pass
