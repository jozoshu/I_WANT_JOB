import psycopg2 as pg2

from config import Env


class DBConnection:
    """DB 연결 정보"""

    @staticmethod
    def get_conn():
        return pg2.connect(**Env.get_conn_params())
