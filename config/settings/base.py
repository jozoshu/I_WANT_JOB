import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'), verbose=True)


COUNTRY = os.environ.get('COUNTRY')
TAG_TYPE_ID = os.environ.get('TAG_TYPE_ID')
JOB_SORT = os.environ.get('JOB_SORT')
LOCATIONS = os.environ.get('LOCATIONS')
YEAR = os.environ.get('YEAR')

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_PORT = os.environ.get('DB_PORT')

LOG_HANDLER = os.environ.get('LOG_HANDLER')
