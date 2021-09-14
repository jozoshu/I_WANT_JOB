import sys


if __name__ == '__main__':
    try:
        from core.arguments import handle_arguments
        handle_arguments(sys.argv)
    except Exception as e:
        raise e
