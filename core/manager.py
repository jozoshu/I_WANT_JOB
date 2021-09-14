from typing import List

from config.logging import get_logger
from config.logging.utils import manager_logging
from modules.handlers.base import BaseHandler
from modules import handlers

logger = get_logger(__name__)


class HandleManager:
    """각 Handler 들이 정상적으로 작동하도록 관리"""

    def __init__(self):
        self.handlers: List = []
        self.scan_handlers()

    def scan_handlers(self):
        for attr in dir(handlers):
            handler = getattr(handlers, attr)
            try:
                assert issubclass(handler, BaseHandler), \
                    f'Invalid Handler Format: {repr(handler)}'
                self.handlers.append(handler())
            except AssertionError as e:
                raise e
            except TypeError:
                pass

    @manager_logging
    def handle(self, *args, **kwargs):
        for handler in self.handlers:
            try:
                logger.info(f'<{handler.__class__.__name__}> - START')
                handler.handle(*args, **kwargs)
                logger.info(f'<{handler.__class__.__name__}> - COMPLETE')
            except Exception as e:
                logger.exception(f'<{handler.__class__.__name__}> - EXCEPTION: {e}')
