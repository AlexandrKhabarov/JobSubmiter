#!/bin/sh

nohup celery -A wsgi_gunicorn:celery_app worker &
gunicorn -c config/gunicorn.conf wsgi_gunicorn:app