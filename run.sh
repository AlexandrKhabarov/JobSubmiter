#!/usr/bin/env bash

nohup celery -A wsgi_gunicorn:celery_app worker &
gunicorn -c config/gun.conf wsgi_gunicorn:app