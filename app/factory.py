from flask import Flask

from app.api.v1.routes import blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint, url_prefix="/v1")

    return app
