import jenkins
from celery import Celery

celery_app = Celery(__name__)


@celery_app.task
def submit_async_job(args):
    server = jenkins.Jenkins('http://localhost:8080')
    server.build_job(name=args['name'], token=args['token'], parameters=args['parameters'])
