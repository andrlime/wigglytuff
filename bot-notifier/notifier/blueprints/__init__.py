"""
All blueprints imported in one module
"""

from dataclasses import dataclass

from flask import Blueprint

from .root.api import bp as root
from .health.api import bp as health


@dataclass
class BlueprintWrapper:
    path: str
    blueprint: Blueprint


def all_blueprints() -> list[BlueprintWrapper]:
    return [
        BlueprintWrapper(path="", blueprint=root),
        BlueprintWrapper(path="health", blueprint=health),
    ]
