from app.base import create_app
from app.task.task import celery_app
from config.config import Mode

app = create_app(Mode.PRODUCTION)
celery_app.conf.update({
    "broker_url": app.config['CELERY_BROKER_URL'],
    "result_backend": app.config['CELERY_RESULT_BACKEND']
})
app.app_context().push()
