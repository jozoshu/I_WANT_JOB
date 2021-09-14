import os
import sys


def env_info(logger):
    """
    :Description
        실행한 환경 출력

    :Info
        Root Dir: 실행되는 위치
        Python: python 버전
        DB Host: 연결한 데이터베이스 host
        DB Name: 연결한 데이터베이스명
    """
    logger.info(f'## - ENV INFO - ##')
    root_dir = os.environ.get('PWD')
    logger.info(f'Root Dir: {root_dir}')
    env = os.environ.get('CRAWLER_DEFAULT_ENV')
    logger.info(f'ENVIRONMENT: {env}')
    version = '.'.join(map(str, sys.version_info[:3]))
    logger.info(f'Python: {version}')
    db_host = os.environ.get('DB_HOST')
    logger.info(f'DB Host: {db_host}')
    db_name = os.environ.get('DB_NAME')
    logger.info(f'DB NAME: {db_name}')
