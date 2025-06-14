"""
App config singleton class
"""

import os

from typing import Any

from dotenv import load_dotenv

from scraper.core.yml_reader import read_yaml_file
from scraper.core.cli import AppCLI
from scraper.core.exceptions import (
    ConfigValueError,
    CLIValueError,
    EnvironmentValueError,
)


class AppConfig(object):
    """
    Singleton AppConfig class to read config from .env and config.yml and
    return a single dictionary with those values
    """

    def __new__(cls) -> "AppConfig":
        if not hasattr(cls, "instance"):
            cls.instance = super(AppConfig, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if hasattr(self, "config"):
            return

        cli_instance = AppCLI()
        load_dotenv()

        config_file = cli_instance.get_parameter_by_key("config")
        yml_config = read_yaml_file(config_file)
        rabbitmq_config = yml_config.get("rabbitmq")
        if rabbitmq_config is None:
            raise ConfigValueError(
                f"Expected non-empty RabbitMQ config in {config_file}, got None"
            )

        self.config = {
            "config": yml_config,
            "rabbitmq": rabbitmq_config,
            "env": os.environ,
            "cli": cli_instance.get_parameters(),
        }

    def get_rmq_variable(self, key: str) -> Any:
        try:
            config = self.config.get("rabbitmq")
            if config is None:
                raise ConfigValueError("RabbitMQ environment doesn't exist")
            value_of_key = config.get(key, False)
            if not value_of_key:
                raise ConfigValueError(f"Key {key} missing in RabbitMQ config")
            return config.get(key)
        except ValueError as e:
            raise ConfigValueError("RabbitMQ config value not found") from e

    def get_config_variable(self, key: str) -> Any:
        try:
            config = self.config.get("config")
            if config is None:
                raise ConfigValueError("Config environment doesn't exist")
            value_of_key = config.get(key, False)
            if not value_of_key:
                raise ConfigValueError(f"Key {key} missing in config")
            return config.get(key)
        except ValueError as e:
            raise ConfigValueError("Config value not found") from e

    def get_cli_argument(self, key: str) -> Any:
        try:
            cli_instance = self.config.get("cli")
            if cli_instance is None:
                raise CLIValueError("CLI environment doesn't exist")
            return cli_instance.get(key, None)
        except ValueError as e:
            raise CLIValueError("CLI value not found") from e

    def get_environment_variable(self, key: str) -> Any:
        try:
            environ = self.config.get("env")
            if environ is None:
                raise EnvironmentValueError("ENV environment doesn't exist")
            value_of_key = environ.get(key, False)
            if not value_of_key:
                raise EnvironmentValueError(f"Key {key} missing in ENV")
            return environ.get(key)
        except ValueError as e:
            raise EnvironmentValueError("Environment variable not found") from e

    def __str__(self) -> str:
        return str(self.config)
