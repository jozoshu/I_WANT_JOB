from .base import *


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s'
        }
    },
    'handlers': {
        'file_info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': f'{BASE_DIR}/logs/info.log',
        }
    },
    'loggers': {
        'main': {
            'handlers': ['file_info'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
