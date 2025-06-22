"""
Error class for when RabbitMQ fails
"""

from notifier.core.exceptions.value_error_wrapper import ValueErrorWrapper


class RabbitMQError(ValueErrorWrapper):
    pass
