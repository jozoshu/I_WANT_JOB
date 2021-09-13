import psycopg2 as pg2

from config import settings


class DBConnection:
    """DB 연결 정보"""

    @staticmethod
    def get_conn():
        return pg2.connect(
            host=settings.DB_HOST,
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            port=settings.DB_PORT,
        )
