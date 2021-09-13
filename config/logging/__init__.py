import logging as _logging
import logging.config

from config import settings


class Logging:
    """로깅 모듈"""

    DEFAULT_FMT = '[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s'
    DEFAULT_FILENAME = f'{settings.BASE_DIR}/logs/info.log'
    DEFAULT_MAX_BYTES = 1024 * 1024 * 1  # 1MB

    def __init__(self):
        config = self._set_parameter(settings.LOGGING)
        _logging.config.dictConfig(config)

    def _scan_modules_dir(self):
        return ['modules.handlers.wanted']

    def _set_parameter(self, logging_env):
        loggers = logging_env['loggers'].get('main')

        for log in self._scan_modules_dir():
            logging_env['loggers'].update({log: loggers})

        return logging_env

    def get_logger(self, name):
        return _logging.getLogger(name)


l = Logging()


def get_logger(name: str = None):
    return l.get_logger(name)
