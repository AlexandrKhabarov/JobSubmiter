import os
from enum import auto, Enum


class Mode(Enum):
    DEVELOPMENT = auto()
    PRODUCTION = auto()
    TEST = auto()


class CommonMode:
    _DEFAULT_JENKINS_HOST = "http://localhost:8080"

    def __init__(self):
        self.JENKINS_HOST = self._get_jenkins_url()

    def _get_jenkins_url(self):
        return self._env_or_default("JENKINS_HOST", self._DEFAULT_JENKINS_HOST)

    @staticmethod
    def _env_or_default(env, default):
        try:
            return os.environ[env]
        except KeyError:
            return default


class TestConfig(CommonMode):
    def __init__(self):
        super().__init__()
        self.DEBUG = False
        self.TESTING = True


class DevelopmentConfig(CommonMode):
    def __init__(self):
        super().__init__()
        self.DEBUG = True


class ProductionConfig(CommonMode):
    def __init__(self):
        super().__init__()
        self.DEBUG = False
        self.SECRET_KEY = "secret_key"
