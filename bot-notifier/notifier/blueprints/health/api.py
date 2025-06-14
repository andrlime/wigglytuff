"""
API route health check
"""

from http import HTTPStatus

from flask import Blueprint, Response
from flask_cors import cross_origin

from notifier.core.util import make_json_response

bp = Blueprint("health", __name__)


@bp.route("/", methods=["GET"])
@cross_origin()
def get_root_page() -> Response:
    """
    Template route
    """

    return make_json_response(f"Health check ping for {__name__}", HTTPStatus.OK)
