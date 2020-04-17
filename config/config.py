import os
from enum import auto, Enum


class Mode(Enum):
    DEVELOPMENT = auto()
    PRODUCTION = auto()


class CommonMode:
    DEFAULT_REDIS_HOST = "127.0.0.1"
    DEFAULT_REDIS_PORT = 6379
    DEFAULT_REDIS_DB = 1

    def __init__(self):
        self.DEBUG = True
        self.REDIS_HOST = self._get_redis_host()
        self.REDIS_PORT = self._get_redis_port()
        self.REDIS_DB = self._get_redis_db()
        self.CELERY_BROKER_URL = self._get_celery_broker_url()
        self.CELERY_RESULT_BACKEND = self.CELERY_BROKER_URL

    def _get_redis_host(self):
        return self._env_or_default("REDIS_HOST", self.DEFAULT_REDIS_HOST)

    def _get_redis_port(self):
        return self._env_or_default("REDIS_PORT", self.DEFAULT_REDIS_PORT)

    def _get_redis_db(self):
        return self._env_or_default("REDIS_DB", self.DEFAULT_REDIS_DB)

    def _get_celery_broker_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @staticmethod
    def _env_or_default(env, default):
        try:
            return os.environ[env]
        except KeyError:
            return default


class DevelopmentMode(CommonMode):
    pass


class ProductionMode(CommonMode):
    def __init__(self):
        super().__init__()
        self.DEBUG = False
        self.SECRET_KEY = "secret_key"
