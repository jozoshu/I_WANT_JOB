import os


env = os.environ.get('ENV')

lib = __import__(f'config.settings.{env}', fromlist=['*'])

for k in dir(lib):
    locals()[k] = getattr(lib, k)
