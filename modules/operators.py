from typing import Dict
from datetime import date, datetime

from psycopg2 import sql

from config.connections.db import DBConnection as db


class Operator:
    """SQL 작업 오퍼레이터"""

    @staticmethod
    def initialize_collecting_process(handler_type: str, conn=None):
        """상태 테이블 초기화"""
        pg_conn = conn or db.get_conn()

        query = """
        DELETE FROM {table} WHERE handler_type=%(handler_type)s
        """
        params = {'handler_type': handler_type}
        with pg_conn.cursor() as cur:
            cur.execute(sql.SQL(query).format(table=sql.Identifier('tb_op_process_listing')), params)
            cur.execute(sql.SQL(query).format(table=sql.Identifier('tb_op_process_collecting')), params)

        if conn is None:
            pg_conn.commit()

    @staticmethod
    def insert_collecting_list(handler_type: str, params: Dict, conn=None):
        """상세정보 상태 테이블에 입력"""
        pg_conn = conn or db.get_conn()

        query = """
        INSERT  INTO {table} (handler_type, position_id, position, company)
        SELECT  *
        FROM (
                SELECT  %(handler_type)s AS handler_type
                      , UNNEST(%(position_id)s::int[]) AS position_id
                      , UNNEST(%(position)s) AS position
                      , UNNEST(%(company)s) AS company
        ) AS a
        """
        params.update({'handler_type': handler_type})
        with pg_conn.cursor() as cur:
            cur.execute(sql.SQL(query).format(table=sql.Identifier('tb_op_process_collecting')), params)

        if conn is None:
            pg_conn.commit()

    @staticmethod
    def set_process_listing_status(handler_type: str, idx: int, status: int, conn=None):
        """수집 리스트 상태 테이블 status 설정"""
        pg_conn = conn or db.get_conn()

        query = """
        INSERT  INTO {table} (handler_type, idx, status)
        VALUES  (%(handler_type)s, %(idx)s, %(status)s)
        """
        params = {
            'handler_type': handler_type,
            'idx': idx,
            'status': status,
        }
        with pg_conn.cursor() as cur:
            cur.execute(sql.SQL(query).format(table=sql.Identifier('tb_op_process_listing')), params)

        if conn is None:
            pg_conn.commit()

    @staticmethod
    def set_process_collecting_status(handler_type: str, position_id: int, status: int, conn=None):
        """상세정보 상태 테이블 status 설정"""
        pg_conn = conn or db.get_conn()

        query = """
        UPDATE  {table}
        SET     status = %(status)s, updated_dtm = now()
        WHERE   handler_type = %(handler_type)s
        AND     position_id = %(position_id)s
        """
        params = {
            'status': status,
            'handler_type': handler_type,
            'position_id': position_id,
        }
        with pg_conn.cursor() as cur:
            cur.execute(sql.SQL(query).format(table=sql.Identifier('tb_op_process_collecting')), params)

        if conn is None:
            pg_conn.commit()

    @staticmethod
    def scan_position_list(handler_type, conn=None):
        """handler_type 에 맞는 수집 리스트 가져오기"""
        pg_conn = conn or db.get_conn()

        query = """
        SELECT  position_id
        FROM    {table}
        WHERE   handler_type = %(handler_type)s
        AND     status IN (0, 500)
        ORDER BY id
        """
        params = {'handler_type': handler_type}
        with pg_conn.cursor() as cur:
            cur.execute(sql.SQL(query).format(table=sql.Identifier('tb_op_process_collecting')), params)
            return cur.fetchall()

    @staticmethod
    def insert_wanted_position_list(params: Dict = None, conn=None):
        """Wanted 공고 리스트 입력"""
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
    def insert_wanted_position_detail(params: Dict, crawl_date: date = None, conn=None):
        """Wanted 채용공고 상세 정보 입력"""
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

    @staticmethod
    def update_last_crawl_date(handler_type: str = None, crawl_date: date = None, conn=None):
        """마지막 수집일 설정"""
        assert handler_type, 'The `handler_type` Must Not Be Null!'

        pg_conn = conn or db.get_conn()

        query = """
        UPDATE  {table}
        SET     last_crawl_date = %(crawl_date)s
        WHERE   handler_type = %(handler_type)s
        """
        params = {
            'crawl_date': crawl_date or datetime.now(),
            'handler_type': handler_type,
        }
        with pg_conn.cursor() as cur:
            cur.execute(sql.SQL(query).format(table=sql.Identifier('tb_op_last_crawl_date')), params)

        if conn is None:
            pg_conn.commit()
