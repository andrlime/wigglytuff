"""
Helper functions to get stuff out of responses
"""

from typing import Any

from notifier.core.exceptions import RequestValueError


def get_body_field(body: Any, key: str) -> Any:
    """
    Encode a message into a JSONified response
    """

    if key not in dict(body):
        raise RequestValueError(f"{key} not found in request body")

    return body.get(key)
