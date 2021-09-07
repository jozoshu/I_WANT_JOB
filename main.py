import os
from pathlib import Path

from dotenv import load_dotenv

from modules.env import Env
from modules.handlers.wanted import WantedHandler
from modules.manager import HandleManager

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'), verbose=True)


def main():
    """
    :Description
        메인 동작 함수

    :Logic
        1. 환경변수를 읽어와서 채용공고를 검색할 파라미터 세팅
        2. 각 handler 실행히여 정보 수집
    """

    params = Env.get_search_params()
    manager = HandleManager()
    manager.add_handler(WantedHandler())
    manager.handle(params=params)


if __name__ == '__main__':
    main()
