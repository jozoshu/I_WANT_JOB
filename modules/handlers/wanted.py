from time import sleep
from typing import Dict

from modules.crawlers.wanted_crawlers import (
    WantedJobListCrawler,
    WantedPositionDetailCrawler
)
from modules.db.operations import Operator as op
from .base import BaseHandler


class WantedHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.validated_params: Dict = {}

    def validate_param(self, params: Dict):
        filtered_params = {
            k: v for k, v in params.items()
            if v != '' and v is not None and k in ['country', 'tag_type_id', 'job_sort', 'locations', 'years']
        }
        self.validated_params = filtered_params

    def _insert_job_list(self, idx):
        if idx:
            self.validated_params.update({'limit': 20, 'offset': 20 * idx})

        try:
            crawler = WantedJobListCrawler()
            response = crawler.crawl(params=self.validated_params)
            op.insert_wanted_position_list(self.conn, response)
            return True
        except Exception as e:
            print(f"Wanted - 크롤링 에러: {e}")
            return False

    def set_job_list(self):
        idx = 30
        is_continue = True
        while is_continue:
            print(f'Wanted - {idx}번째 리스트 crawl')
            is_continue = self._insert_job_list(idx)
            idx += 1
            sleep(.1)
        self.conn.commit()

    def set_position_details(self):
        for position_id, *_ in op.scan_wanted_position_list():
            try:
                crawler = WantedPositionDetailCrawler()
                response = crawler.crawl(position_id=position_id)
                op.insert_wanted_position_detail(self.conn, response)
                print(f'Wanted - 채용 상세 정보 저장 - {position_id}')
            except Exception as e:
                print(f'Wanted - 채용 상세 정보 저장 에러 - {position_id} - {e}')
            finally:
                sleep(.1)
        self.conn.commit()

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
