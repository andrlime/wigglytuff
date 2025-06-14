"""
Helper functions to configure Flask app settings
"""

import os
from typing import Any

from dotenv import load_dotenv
from yaml import Loader, load

from notifier.core.exceptions import ConfigValueError, EnvironmentValueError


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
        if not hasattr(self, "config"):
            load_dotenv()

            yml_config = self.read_yaml_config_file("config.yaml")
            app_config = yml_config.get("app")

            self.config = {
                "app_port": self.get_key(app_config, "app_port", "config.yml"),
                "env": os.environ,
            }

    def get_key(self, obj: dict, key: str, place: str) -> Any:
        try:
            return obj.get(key)
        except ValueError as e:
            raise ConfigValueError(f"{key} not set in {place}") from e

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

    def read_yaml_config_file(self, path: str) -> Any:
        """
        Read DB config from the config.yml file
        """

        stream = open(path, "r", encoding="utf-8")
        content = load(stream, Loader)
        stream.close()

        return content
