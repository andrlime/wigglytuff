"""
Error class for when an environment value has an error
"""

from .config_value_error import ConfigValueError


class EnvironmentValueError(ConfigValueError):
    pass
