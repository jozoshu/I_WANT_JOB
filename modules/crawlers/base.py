from abc import ABC, abstractmethod
from typing import Dict

import requests


class BaseCrawler(ABC):
    """베이스 크롤러"""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def request_get(self, params: Dict = None, **kwargs) -> Dict:
        res = requests.get(url=self.base_url, params=params, **kwargs)
        if res.status_code == 200:
            return res.json()
        raise ValueError(f'서버 통신 Error {self.base_url} - [{res.status_code}] {res.reason}')

    def request_post(self, data: str = None, json: Dict = None, **kwargs) -> Dict:
        res = requests.post(url=self.base_url, data=data, json=json, **kwargs)
        if res.status_code == 200:
            return res.json()
        raise ValueError(f'서버 통신 Error {self.base_url} - [{res.status_code}] {res.reason}')

    @abstractmethod
    def crawl(self, *args, **kwargs):
        """크롤링 실행"""
        raise NotImplementedError('You Must Implement `crawl` Method.')
