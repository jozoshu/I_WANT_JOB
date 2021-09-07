import logging

from config import Env


class Logging:

    DEFAULT_FMT = '[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s'

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
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(self.DEFAULT_FMT)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    @property
    def logger(self):
        return self._logger


def get_logger(name: str = None):
    return Logging(name).logger
