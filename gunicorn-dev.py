#IP Bind location
bind = "0.0.0.0:5010"
backlog = 256

#Performance
workers = 2
worker_connections = 100
timeout = 60
keepalive = 2

#development
reload = True

#Logging
errorlog = '-'
loglevel = 'debug'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
