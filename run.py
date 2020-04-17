from app.base import create_app, setup_celery
from app.task.task import celery_app
from config.config import Mode

app = create_app(Mode.DEVELOPMENT)
celery_app = setup_celery(celery_app, app)

if __name__ == "__main__":
    app.run()
