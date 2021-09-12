import logging
from logging.handlers import RotatingFileHandler

from config import BASE_DIR, Env


class Logging:
    """로깅 모듈"""

    DEFAULT_FMT = '[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s'
    DEFAULT_FILENAME = f'{BASE_DIR}/logs/info.log'
    DEFAULT_MAX_BYTES = 1024 * 1024 * 1  # 1MB

    def __init__(self, name: str = None):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

        logging_args = Env.get_logging_args()
        self._set_handlers(logging_args)

    def _set_handlers(self, logging_args):
        handlers = logging_args.get('handlers').split(',')

        file_handler = [x for x in handlers if x in ['FileHandler', 'RotatingFileHandler']]
        if len(file_handler) > 1:
            _handler = ', '.join(file_handler)
            raise ValueError(f'You can choose just one File Handler, But: {_handler} in `LOG_HANDLER`')

        for handler in map(lambda x: x.lower(), handlers):
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
