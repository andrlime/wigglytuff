"""
App factory to create a Flask app object
"""

from flask import Flask
from flask_cors import CORS

from notifier.blueprints import all_blueprints


def create_flask_app() -> Flask:
    """
    Creates a Flask app object
    """

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    for bp in all_blueprints():
        app.register_blueprint(bp.blueprint, url_prefix=f"/{bp.path}")

    return app
