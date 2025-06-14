"""
CLI class that reads specific arguments for use by LLM resume generator
"""

from typing import AnyStr

import argparse
import os
import sys
import pathlib

from scraper.core.exceptions import CLIValueError, PathError


def argv() -> list[str]:
    return sys.argv[1:]


class AppCLI:
    """
    Singleton CLI class to read arguments from an array of strings
    """

    def __new__(cls) -> "AppCLI":
        if not hasattr(cls, "instance"):
            cls.instance = super(AppCLI, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if hasattr(self, "args"):
            return

        arguments = argv()

        parser = argparse.ArgumentParser(
            prog="scraper",
            description="""
Fetches jobs from remote APIs every (interval, defined in config) seconds and enqueues them into RabbitMQ for consumption by a variety of consumers
            """,
        )

        parser.add_argument(
            "-c",
            "--config",
            help="Path to config.yml/config.yaml file",
            type=pathlib.Path,
            required=True,
        )

        self.args = parser.parse_args(arguments)
        self.lint()

    def lint(self) -> None:
        arguments = self.args

        if not os.path.isfile(arguments.config):
            raise PathError(f"Invalid config file {arguments.config}")

    def get_parameters(self) -> dict[str, str]:
        return vars(self.args)

    def get_parameter_by_key(self, key: AnyStr) -> str:
        try:
            key_str = str(key)
            return str(vars(self.args)[key_str])
        except ValueError as e:
            raise CLIValueError(f"CLI does not contain key {str(key)}") from e

    def get_path_by_key(self, key: AnyStr) -> str:
        path = self.get_parameter_by_key(key)
        return os.path.abspath(path)
