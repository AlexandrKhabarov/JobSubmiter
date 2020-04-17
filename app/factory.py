import os

from celery import Celery
from flask import Flask

from app.api.v1.routes import blueprint
from app.task.task import celery_app


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint, url_prefix="/api/v1")

    app.config['REDIS_DB'] = os.environ["REDIS_DB"]
    app.config['REDIS_HOST'] = os.environ["REDIS_HOST"]
    app.config['REDIS_PORT'] = os.environ["REDIS_PORT"]
    app.config['CELERY_BROKER_URL'] = os.environ["CELERY_BROKER_URL"]
    app.config['CELERY_RESULT_BACKEND'] = os.environ["CELERY_RESULT_BACKEND"]

    celery_conf = f"redis://{app.config['REDIS_HOST']}:{app.config['REDIS_PORT']}/{app.config['REDIS_DB']}"
    celery_app.conf.update({'broker_url': celery_conf, 'result_backend': celery_conf})

    return app


def create_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    return celery
