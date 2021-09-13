import os


class ArgumentHandler:
    def __init__(self, args):
        self.argument_list = args[1:]
        self.arg_dict = {}

    def _validate_key(self, key: str):
        if not key.startswith('--'):
            raise ValueError(f'Invalid Argument: {key}')
        return key[2:]

    def parse(self):
        for argument in self.argument_list:
            k, *v = argument.split('=')
            key = self._validate_key(k)
            self.arg_dict.update({key: v})

    def processing(self):
        for k, v in self.arg_dict.items():
            if k == 'env':
                os.environ.setdefault('CRAWLER_DEFAULT_ENV', v[0])

    @staticmethod
    def set_default():
        os.environ.setdefault('CRAWLER_DEFAULT_ENV', 'local')

    def handle(self):
        self.parse()
        self.processing()
        self.set_default()


def handle_arguments(args):
    h = ArgumentHandler(args)
    h.handle()
