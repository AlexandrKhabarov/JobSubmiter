#!/bin/sh

gunicorn -c config/gunicorn.conf wsgi:app