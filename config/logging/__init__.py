import os
from typing import Dict, List

import logging as _logging
import logging.config

from config import settings


class Logging:
    """로깅 모듈"""

    def __init__(self):
        global _logging
        self.module_list = []
        config = self.set_loggers(settings.LOGGING)
        _logging.config.dictConfig(config)

    def _process_filename(self, filename: str) -> str:
        filename = filename.replace('/', '.').replace('__init__', '')
        if filename.endswith('.'):
            filename = filename[:-1]
        return filename

    def _scan_modules_dir(self) -> List:
        module_list = ['core.manager']
        for parent, _, file_list in os.walk(f'modules'):
            for fname in map(lambda x: x[:-3], filter(lambda x: x.endswith('.py'), file_list)):
                name = self._process_filename(f'{parent}/{fname}')
                module_list.append(name)
        return module_list

    def set_loggers(self, logging_env: Dict) -> Dict:
        loggers = logging_env['loggers'].get('main')

        for log in self._scan_modules_dir():
            logging_env['loggers'].update({log: loggers})

        return logging_env

    def get_logger(self, name: str):
        return _logging.getLogger(name)


l = Logging()


def get_logger(name: str = None):
    return l.get_logger(name)
