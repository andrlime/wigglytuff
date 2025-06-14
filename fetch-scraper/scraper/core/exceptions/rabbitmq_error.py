"""
Error class for when RabbitMQ fails
"""

from scraper.core.exceptions.value_error_wrapper import ValueErrorWrapper


class RabbitMQError(ValueErrorWrapper):
    pass
