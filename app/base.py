from flask import Flask

from app.api.v1.routes import blueprint
from config.config import Mode, DevelopmentMode, ProductionMode
from config.exceptions import UnrecognizedMode


def create_app(mode):
    app = Flask(__name__)
    app.register_blueprint(blueprint, url_prefix="/api/v1")

    if mode == Mode.DEVELOPMENT:
        config = DevelopmentMode()
        app.config.from_object(config)
    elif mode == Mode.PRODUCTION:
        config = ProductionMode()
        app.config.from_object(config)
    else:
        raise UnrecognizedMode(mode)

    return app


def setup_celery(celery, app):
    celery.conf.update({
        "broker_url": app.config['CELERY_BROKER_URL'],
        "result_backend": app.config['CELERY_RESULT_BACKEND']
    })
    return celery
