import logging
from logging.handlers import RotatingFileHandler

from config import Env


class Logging:
    """로깅 모듈"""

    DEFAULT_FMT = '[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s'
    DEFAULT_FILENAME = 'logs/info.log'
    DEFAULT_MAX_BYTES = 1024 * 1024 * 1  # 1MB

    def __init__(self, name: str = None):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

        logging_args = Env.get_logging_args()
        handlers = map(lambda x: x.lower(), logging_args.get('handlers').split(','))

        for handler in handlers:
            func = getattr(self, f'add_{handler}', None)
            if not func:
                raise ValueError('Invalid `LOG_HANDLER`')
            func()

    def add_streamhandler(self):
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter(self.DEFAULT_FMT)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def add_filehandler(self, filename: str = None):
        filename = filename or self.DEFAULT_FILENAME
        handler = logging.FileHandler(filename, mode='a')
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter(self.DEFAULT_FMT)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def add_rotatingfilehandler(self, filename: str = None):
        filename = filename or self.DEFAULT_FILENAME
        handler = RotatingFileHandler(
            filename, mode='a', maxBytes=self.DEFAULT_MAX_BYTES, backupCount=100
        )
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter(self.DEFAULT_FMT)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    @property
    def logger(self):
        return self._logger


def get_logger(name: str = None):
    return Logging(name).logger
