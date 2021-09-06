import os


class Config:
    """크롤링에 파라미터 관리"""

    @staticmethod
    def get_params():
        return {
            'country': os.environ.get('COUNTRY'),
            'tag_type_id': os.environ.get('TAG_TYPE_ID'),
            'job_sort': os.environ.get('JOB_SORT'),
            'locations': os.environ.get('LOCATIONS'),
            'years': os.environ.get('YEAR'),
        }
