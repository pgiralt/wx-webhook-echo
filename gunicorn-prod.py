#IP Bind location
bind = "0.0.0.0:9189"
backlog = 2048

#Performance
workers = 1
worker_connections = 100
timeout = 60
keepalive = 2

#Reload on changes
reload = True


#Logging
errorlog = '/var/log/sites/acronymbot/error.log'
loglevel = 'info'
accesslog = '/var/log/sites/acronymbot/access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'