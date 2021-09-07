from functools import wraps

from . import get_logger
from .utils import env_info


def manager_logging(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger('main')
        env_info(logger)

        logger.info('RUNNING MANAGER')
        logger.info('='*80)
        func(*args, **kwargs)
        logger.info('='*80)
        logger.info('FINISHED')

    return wrapper
