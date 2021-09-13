from config import settings


class SearchParams:
    @staticmethod
    def get_search_params():
        return {
            'country': settings.COUNTRY,
            'tag_type_id': settings.TAG_TYPE_ID,
            'job_sort': settings.JOB_SORT,
            'locations': settings.LOCATIONS,
            'years': settings.YEAR,
        }
