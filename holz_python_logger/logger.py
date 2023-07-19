import logging
import socket

from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.transport import TcpTransport

from .settings import PROJECT_NAME, LOG_LEVEL, LOGSTASH_HOST, LOGSTASH_PORT, ENVIRONMENT


HOSTNAME = socket.gethostname()

logger = logging.getLogger("python-logstash-logger")
logger.setLevel(LOG_LEVEL)

if not LOGSTASH_HOST or not LOGSTASH_PORT:
    raise ValueError('LOGSTASH_HOST MUST BE SET')

handler = AsynchronousLogstashHandler(
    LOGSTASH_HOST,
    LOGSTASH_PORT,
    transport=TcpTransport(
        LOGSTASH_HOST,
        LOGSTASH_PORT,
        timeout=5.0,
        ssl_enable=False,
        ssl_verify=False,
        keyfile=None,
        certfile=None,
        ca_certs=None
    ),
    database_path=None,
)

logger.addHandler(handler)


class HolzLogger:
    def __init__(self, logger_):
        self._logger = logger_

    @staticmethod
    def _extend_kwargs(**kwargs):
        if 'extra' in kwargs:
            kwargs['extra']['project'] = PROJECT_NAME
        else:
            kwargs['extra'] = {'project': PROJECT_NAME}

        kwargs['extra']['hostname'] = HOSTNAME
        kwargs['extra']['environment'] = ENVIRONMENT
        return kwargs

    def _log(self, level, msg, *args, **kwargs):
        kwargs = self._extend_kwargs(**kwargs)
        self._logger.log(level, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log(logging.INFO, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._log(logging.DEBUG, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._log(logging.ERROR, msg, *args, **kwargs)

    def exception(self, exc, *args, **kwargs):
        kwargs = self._extend_kwargs(**kwargs)
        self._logger.exception(exc, *args, **kwargs)


holz_logger = HolzLogger(logger)
