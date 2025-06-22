"""
Error class for when a configuration value has an error
"""

from notifier.core.exceptions.value_error_wrapper import ValueErrorWrapper


class ConfigValueError(ValueErrorWrapper):
    pass
