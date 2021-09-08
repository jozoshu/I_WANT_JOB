from abc import ABC, abstractmethod
from datetime import datetime

from pytz import timezone

from config.db.connections import DBConnection as db
from modules.operators import Operator as op

KST = timezone('Asia/Seoul')


class BaseHandler(ABC):
    """베이스 handler"""

    def __init__(self):
        self._conn = db.get_conn()
        self.crawl_date = KST.localize(datetime.now()).date()

    @property
    def conn(self):
        return self._conn

    @property
    def NAME(self):
        raise NotImplementedError('You Must Define `NAME` Property.')

    @property
    def name(self):
        return self.NAME

    @abstractmethod
    def handle(self, *args, **kwargs):
        """handler 실행"""
        raise NotImplementedError('You Must Implement `handle` Method.')

    def update_last_crawl_date(self):
        """최근 수집날짜 저장"""
        op.update_last_crawl_date(self.conn, self.name, self.crawl_date)
        self.conn.commit()
