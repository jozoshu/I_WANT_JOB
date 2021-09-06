from abc import ABC, abstractmethod

from modules.db.connections import DBConnection as db


class BaseHandler(ABC):
    """베이스 handler"""

    def __init__(self):
        self._conn = db.get_conn()

    @property
    def conn(self):
        return self._conn

    @abstractmethod
    def handle(self, *args, **kwargs):
        """handler 실행"""
        raise NotImplementedError('You Must Implement `handle` Method.')
