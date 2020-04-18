from flask import Flask

from app.api.v1.routes import blueprint
from app.utils.jenkins import Jenkins
from config.config import Mode, DevelopmentConfig, ProductionConfig, TestConfig
from app.exceptions import UnrecognizedMode


def create_config(mode):
    if mode == Mode.DEVELOPMENT:
        config = DevelopmentConfig()
    elif mode == Mode.PRODUCTION:
        config = ProductionConfig()
    elif mode == Mode.TEST:
        config = TestConfig()
    else:
        raise UnrecognizedMode(mode)

    return config


def create_app(config):
    app = Flask(__name__)
    app.register_blueprint(blueprint, url_prefix="/api/v1")
    app.config.from_object(config)
    return app


def setup_jenkins(jenkins, config):
    jenkins_host = config.JENKINS_HOST
    jenkins.init_url(jenkins_host)


def init(mode):
    config = create_config(mode)
    app = create_app(config)
    setup_jenkins(Jenkins, config)
    return app
