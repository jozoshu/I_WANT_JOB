import sys

from core import execute
from core.arguments import handle_arguments


if __name__ == '__main__':
    handle_arguments(sys.argv)
    execute()
