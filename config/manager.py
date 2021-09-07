from typing import List

from config.logging.decorators import manager_logging
from modules.handlers.base import BaseHandler
from config.logging import get_logger

logger = get_logger(__name__)


class HandleManager:
    """각 Handler 들이 정상적으로 작동하도록 관리"""

    def __init__(self):
        self.handlers: List = []

    def add_handler(self, handler: BaseHandler):
        assert isinstance(handler, BaseHandler)
        self.handlers.append(handler)

    @manager_logging
    def handle(self, *args, **kwargs):
        for handler in self.handlers:
            try:
                logger.info(f'<{handler.__class__.__name__}> - START')
                handler.handle(*args, **kwargs)
                logger.info(f'<{handler.__class__.__name__}> - COMPLETE')
            except Exception as e:
                logger.error(f'<{handler.__class__.__name__}> - EXCEPTION: {e}')
