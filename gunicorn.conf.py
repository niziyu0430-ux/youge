"""One process is required while page-lifetime login sessions are in memory."""
import os

bind = '0.0.0.0:' + os.environ.get('PORT', '10000')
workers = 1
worker_class = 'gthread'
threads = 8
timeout = 120
graceful_timeout = 30
keepalive = 5
accesslog = '-'
errorlog = '-'
# Do not log query strings, authorization headers or submitted answers.
access_log_format = '%(h)s %(m)s %(U)s %(s)s %(L)s'
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
