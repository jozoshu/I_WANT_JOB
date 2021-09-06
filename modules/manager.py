from typing import List

from modules.handlers.base import BaseHandler


class HandleManager:
    """각 Handler 들이 정상적으로 작동하도록 관리"""

    def __init__(self):
        self.handlers: List = []

    def add_handler(self, handler: BaseHandler):
        assert isinstance(handler, BaseHandler)
        self.handlers.append(handler)

    def handle(self, *args, **kwargs):
        for handler in self.handlers:
            try:
                print(f'<{handler.__class__.__name__}> - START')
                handler.handle(*args, **kwargs)
                print(f'<{handler.__class__.__name__}> - COMPLETE')
            except Exception as e:
                print(f'<{handler.__class__.__name__}> - EXCEPTION: {e}')
