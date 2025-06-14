"""
Reads stuff from YAML files
"""

from typing import Any

from yaml import load, Loader


def read_yaml_file(path: str) -> dict[str, Any]:
    stream = open(path, "r", encoding="utf-8")
    content = load(stream, Loader)
    stream.close()

    if not isinstance(content, dict):
        raise TypeError(f"Expected dict, got {type(content).__name__}")
    return content
