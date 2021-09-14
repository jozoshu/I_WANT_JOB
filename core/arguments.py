import os
import sys

from core import execute
from core.versions import get_version


class ArgumentHandler:
    """Command 로 입력받은 argument 읽어와서 알맞은 환경 설정"""

    VALID_ARGS = ['--env', '--version']

    def __init__(self, args):
        self.executable = True
        self.argument_list = args[1:]
        self.arg_dict = {}

    def _validate_key(self, key: str):
        if not key.startswith('--') or key not in self.VALID_ARGS:
            raise ValueError(f'Invalid Argument: {key}')
        return key[2:]

    def parse(self):
        for argument in self.argument_list:
            k, *v = argument.split('=')
            key = self._validate_key(k)
            self.arg_dict.update({key: v})

    def process(self):
        for k, v in self.arg_dict.items():
            if k == 'env':
                os.environ.setdefault('CRAWLER_DEFAULT_ENV', v[0])
            elif k == 'version':
                self.executable = False
                sys.stdout.write(get_version())
                break

    @staticmethod
    def set_default():
        os.environ.setdefault('CRAWLER_DEFAULT_ENV', 'local')

    def handle(self):
        self.parse()
        self.process()
        self.set_default()

        if self.executable:
            execute()


def handle_arguments(args):
    h = ArgumentHandler(args)
    h.handle()
