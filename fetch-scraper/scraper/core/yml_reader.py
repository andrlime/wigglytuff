"""
Reads stuff from YAML files
"""

from yaml import load, Loader


def read_yaml_file(path: str) -> str:
    stream = open(path, "r", encoding="utf-8")
    content = load(stream, Loader)
    stream.close()

    return content
