import jenkins
from celery import Celery

celery_app = Celery(__name__)


@celery_app.task
def submit_async_job(args):
    username = args['username']
    password = args['password']
    server = jenkins.Jenkins('http://jenkins:8080', username, password)
    server.build_job(name=args['name'], parameters=args['parameters'])
