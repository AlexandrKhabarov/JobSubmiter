workers = 4
threads = 4
bind = '0.0.0.0:80'
worker_class = 'eventlet'
worker_connections = 2000
pidfile = 'gunicorn.pid'
accesslog = './logs/access.log'
errorlog = './logs/error.log'
loglevel = 'info'
reload = True
