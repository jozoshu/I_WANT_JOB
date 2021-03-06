from time import sleep
from typing import Dict

from psycopg2 import IntegrityError

from config.logging import get_logger
from modules.crawlers.wanted_crawlers import (
    WantedJobListCrawler,
    WantedPositionDetailCrawler
)
from modules.operators import Operator as op
from .base import BaseHandler

logger = get_logger(__name__)


class WantedHandler(BaseHandler):

    NAME = 'WANTED'

    def __init__(self):
        super().__init__()
        self.validated_params: Dict = {}

    def validate_param(self, params: Dict):
        filtered_params = {
            k: v for k, v in params.items()
            if v != '' and v is not None and k in ['country', 'tag_type_id', 'job_sort', 'locations', 'years']
        }
        self.validated_params = filtered_params

    def _insert_job_list(self, idx: int):
        if idx:
            self.validated_params.update({'limit': 20, 'offset': 20 * idx})

        try:
            crawler = WantedJobListCrawler()
            response = crawler.crawl(params=self.validated_params)
            op.insert_wanted_position_list(response, self.conn)
            op.insert_collecting_list(self.name, response)
            op.set_process_listing_status(self.name, idx, 200, self.conn)
            logger.info(f'Wanted - {idx}번째 리스트 crawl')
            self.conn.commit()
            return True
        except Exception as e:
            op.set_process_listing_status(self.name, idx, 500, self.conn)
            logger.error(f'Wanted - 크롤링 에러: {e}')
            self.conn.commit()
            return False

    def set_job_list(self):
        op.initialize_collecting_process(self.name)

        idx = 0
        is_continue = True
        while is_continue:
            is_continue = self._insert_job_list(idx)
            idx += 1
            sleep(.1)

    def set_position_details(self):
        for position_id, *_ in op.scan_position_list(self.name):
            try:
                crawler = WantedPositionDetailCrawler()
                response = crawler.crawl(position_id=position_id)
                op.insert_wanted_position_detail(response, self.crawl_date)
                op.set_process_collecting_status(self.name, position_id, 200)
                logger.info(f'Wanted - 채용공고 상세 정보 저장 - position_id: {position_id}')
            except IntegrityError as e:
                op.set_process_collecting_status(self.name, position_id, 300)
                logger.info(f'Wanted - 채용공고 상세 정보 저장 DB 에러 - position_id: {position_id} - {e}')
            except Exception as e:
                op.set_process_collecting_status(self.name, position_id, 500)
                logger.exception(f'Wanted - 채용공고 상세 정보 저장 에러 - position_id: {position_id} - {e}')
            finally:
                sleep(.1)

    def handle(self, params: Dict):
        """
        :Description
            1. 검색 파라미터 검증
            2. 원티드 페이지에서 검색 조건에 맞는 공고들 수집
            3. 각 공고별로 채용 상세 정보를 가져와서 저장
        """
        self.validate_param(params)
        self.set_job_list()
        self.set_position_details()
        self.update_last_crawl_date()
