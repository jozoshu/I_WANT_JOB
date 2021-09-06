import os

import psycopg2 as pg2


class DBConnection:
    """DB 연결 정보"""

    @staticmethod
    def get_conn():
        return pg2.connect(
            host=os.environ.get('DB_HOST'),
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            port=os.environ.get('DB_PORT')
        )
