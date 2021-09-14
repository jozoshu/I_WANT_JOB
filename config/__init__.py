import os

env = os.environ.get('CRAWLER_DEFAULT_ENV')


class Settings:
    _lib = __import__(f'config.settings.{env}', fromlist=['*'])

    for k in dir(_lib):
        locals()[k] = getattr(_lib, k)


settings = Settings()
