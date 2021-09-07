from psycopg2 import sql

from .connections import DBConnection as db


class Operator:
    """SQL 작업 오퍼레이터"""

    @staticmethod
    def insert_wanted_position_list(conn=None, params=None):
        if not conn:
            conn = db.get_conn()

        query = """
        INSERT  INTO {table} (company_id, company, position_id, position, thumbnail, logo)
        SELECT  *
        FROM (
                SELECT  UNNEST(%(company_id)s::int[]) AS company_id,
                        UNNEST(%(company)s) AS company,
                        UNNEST(%(position_id)s::int[]) AS position_id,
                        UNNEST(%(position)s) AS position,
                        UNNEST(%(thumbnail)s) AS thumbnail,
                        UNNEST(%(logo)s) AS logo
        ) AS a
        WHERE   a.position_id NOT IN (
                SELECT  position_id
                FROM    {table}
        )
        """
        with conn.cursor() as cur:
            cur.execute(sql.SQL(query).format(table=sql.Identifier('tb_wtd_position')), params)

    @staticmethod
    def scan_wanted_position_list(conn=None):
        if not conn:
            conn = db.get_conn()

        query = """SELECT position_id FROM {table}"""
        with conn.cursor() as cur:
            cur.execute(sql.SQL(query).format(table=sql.Identifier('tb_wtd_position')))
            return cur.fetchall()

    @staticmethod
    def insert_wanted_position_detail(conn=None, params=None):
        if not conn:
            conn = db.get_conn()

        query = """
        INSERT  INTO {table} 
                (position_id, position, company_id, company, intro, main_tasks, requirements, preferred_points, benefits)
        VALUES  (%(position_id)s, %(position)s, %(company_id)s, %(company)s, %(intro)s, 
                %(main_tasks)s, %(requirements)s, %(preferred_points)s, %(benefits)s)
        """
        with conn.cursor() as cur:
            cur.execute(sql.SQL(query).format(table=sql.Identifier('tb_wtd_position_detail')), params)
