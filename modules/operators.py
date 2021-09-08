from typing import Dict
from datetime import date, datetime

from psycopg2 import sql

from config.db.connections import DBConnection as db


class Operator:
    """SQL 작업 오퍼레이터"""

    @staticmethod
    def insert_wanted_position_list(conn=None, params: Dict = None):
        pg_conn = conn or db.get_conn()

        query = """
        INSERT  INTO {table} (company_id, company, position_id, position, thumbnail, logo)
        SELECT  *
        FROM (
                SELECT  UNNEST(%(company_id)s::int[]) AS company_id
                      , UNNEST(%(company)s) AS company
                      , UNNEST(%(position_id)s::int[]) AS position_id
                      , UNNEST(%(position)s) AS position
                      , UNNEST(%(thumbnail)s) AS thumbnail
                      , UNNEST(%(logo)s) AS logo
        ) AS a
        WHERE   a.position_id NOT IN (
                SELECT  position_id FROM {table}
        )
        """
        with pg_conn.cursor() as cur:
            cur.execute(sql.SQL(query).format(table=sql.Identifier('tb_wtd_position')), params)

        if conn is None:
            pg_conn.commit()

    @staticmethod
    def scan_wanted_position_list(conn=None):
        pg_conn = conn or db.get_conn()

        query = """SELECT position_id FROM {table}"""
        with pg_conn.cursor() as cur:
            cur.execute(sql.SQL(query).format(table=sql.Identifier('tb_wtd_position')))
            return cur.fetchall()

    @staticmethod
    def insert_wanted_position_detail(conn=None, params: Dict = None, crawl_date: date = None):
        pg_conn = conn or db.get_conn()

        query = """
        INSERT  INTO {table} 
                (position_id, position, company_id, company, intro, main_tasks, requirements, preferred_points, benefits, crawl_date)
        VALUES  (%(position_id)s, %(position)s, %(company_id)s, %(company)s, %(intro)s,
                %(main_tasks)s, %(requirements)s, %(preferred_points)s, %(benefits)s, %(crawl_date)s)
        """
        params.update({'crawl_date': crawl_date or datetime.now()})
        with pg_conn.cursor() as cur:
            cur.execute(sql.SQL(query).format(table=sql.Identifier('tb_wtd_position_detail')), params)

        if conn is None:
            pg_conn.commit()