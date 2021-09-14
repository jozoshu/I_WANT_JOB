import os

env = os.environ.get('CRAWLER_DEFAULT_ENV')


class Settings:
    def __init__(self):
        _lib = __import__(f'config.settings.{env}', fromlist=['*'])

        for key in dir(_lib):
            value = getattr(_lib, key)
            setattr(self, key, value)

    def __setattr__(self, key, value):
        if key == 'BASE_DIR':
            os.chdir(value)
        super().__setattr__(key, value)


settings = Settings()
