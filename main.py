import sys

from config.arguments import handle_arguments


def main():
    """
    :Description
        메인 동작 함수

    :Logic
        1. 환경변수를 읽어와서 채용공고를 검색할 파라미터 세팅
        2. 각 handler 실행히여 정보 수집
    """
    from modules.params import SearchParams
    from modules.handlers.wanted import WantedHandler
    from modules.manager import HandleManager
    """
    환경변수가 세팅되기 전 settings 파일을 불러오는걸 방지하기 위해
    함수 내에서 모듈을 불러오도록 구성
    """

    params = SearchParams.get_search_params()
    manager = HandleManager()
    manager.add_handler(WantedHandler())
    manager.handle(params=params)


if __name__ == '__main__':
    handle_arguments(sys.argv)
    main()
