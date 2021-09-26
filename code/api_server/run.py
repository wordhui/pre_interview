import multiprocessing


bind = "0.0.0.0:5000"
timeout = 40

workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
backlog = 2048


worker_class = "uvicorn.workers.UvicornWorker"

worker_connections = 1000

daemon = True

loglevel = 'debug'
pidfile = 'log/gunicorn.pid'
accesslog = 'log/gun-access.log'
errorlog = 'log/gun-error.log'

