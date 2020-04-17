from app.base import create_app
from app.task.task import celery_app
from config.config import Mode

app = create_app(Mode.DEVELOPMENT)
celery_app.conf.update(app.config)

if __name__ == "__main__":
    app.run()
