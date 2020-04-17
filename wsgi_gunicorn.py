from app.base import create_app
from app.task.task import celery_app
from config.config import Mode

app = create_app(Mode.PRODUCTION)
celery_app.conf.update(app.config)
app.app_context().push()
