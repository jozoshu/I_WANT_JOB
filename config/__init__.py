import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'), verbose=True)


class Env:
    """환경변수 관리"""

    @staticmethod
    def get_search_params():
        return {
            'country': os.environ.get('COUNTRY'),
            'tag_type_id': os.environ.get('TAG_TYPE_ID'),
            'job_sort': os.environ.get('JOB_SORT'),
            'locations': os.environ.get('LOCATIONS'),
            'years': os.environ.get('YEAR'),
        }

    @staticmethod
    def get_conn_params():
        return {
            'host': os.environ.get('DB_HOST'),
            'dbname': os.environ.get('DB_NAME'),
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'port': os.environ.get('DB_PORT'),
        }

    @staticmethod
    def get_logging_args():
        return {
            'handlers': os.environ.get('LOG_HANDLER'),
        }
