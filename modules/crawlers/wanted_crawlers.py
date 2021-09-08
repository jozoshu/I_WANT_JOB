from datetime import datetime
import time
from typing import Dict

from .base import BaseCrawler


class WantedJobListCrawler(BaseCrawler):
    """
    :Description
        원티드 채용정보 크롤링

    :Return
        company_id  - 회사 pk
        company     - 회사명
        position_id - 직무 pk
        position    - 직무
        thumbnail   - 썸네일
        logo        - 로고
    """
    def __init__(self):
        base_url = 'https://www.wanted.co.kr/api/v4/jobs'
        super().__init__(base_url)

    def crawl(self, params: Dict) -> Dict:
        res_json = self.request_get(params, timeout=10)
        if not res_json['data']:
            raise ValueError('더 이상 채용공고 없음')
        return {
            'company_id': [data['company']['id'] for data in res_json['data']],
            'company': [data['company']['name'] for data in res_json['data']],
            'position_id': [data['id'] for data in res_json['data']],
            'position': [data['position'] for data in res_json['data']],
            'thumbnail': [data['title_img']['origin'] for data in res_json['data']],
            'logo': [data['logo_img']['origin'] for data in res_json['data']],
        }


class WantedPositionDetailCrawler(BaseCrawler):
    """
    :Description
        직무 상세정보 크롤링

    :Return
        position_id      - 직무 pk
        position         - 직무
        company_id       - 회사 pk
        company          - 회사명
        intro            - 회사소개
        main_tasks       - 주요업무
        requirements     - 자격요건
        preferred_points - 우대사항
        benefits         - 혜택 및 복지
    """
    def __init__(self):
        base_url = 'https://www.wanted.co.kr/api/v4/jobs/{position_id}?{timestamp}'
        super().__init__(base_url)

    def _set_base_url(self, position_id: int):
        timestamp = time.mktime(datetime.now().timetuple()) * 1000
        self.base_url = self.base_url.format(position_id=position_id, timestamp=int(timestamp))

    def crawl(self, position_id: int) -> Dict:
        self._set_base_url(position_id)
        res_json = self.request_get(timeout=10)
        return {
            'position_id': position_id,
            'position': res_json['job']['position'],
            'company_id': res_json['job']['company']['id'],
            'company': res_json['job']['company']['name'],
            'intro': res_json['job']['detail']['intro'],
            'main_tasks': res_json['job']['detail']['main_tasks'],
            'requirements': res_json['job']['detail']['requirements'],
            'preferred_points': res_json['job']['detail']['preferred_points'],
            'benefits': res_json['job']['detail']['benefits'],
        }
