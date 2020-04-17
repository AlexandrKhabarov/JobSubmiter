from app.base import create_app, setup_celery
from app.task.task import celery_app
from config.config import Mode

app = create_app(Mode.PRODUCTION)
celery_app = setup_celery(celery_app, app)
