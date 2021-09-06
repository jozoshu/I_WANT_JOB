import os
from pathlib import Path

from dotenv import load_dotenv

from modules.config import Config
from modules.handlers.wanted import WantedHandler
from modules.manager import HandleManager

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'), verbose=True)


def main():
    """메인 동장 함수"""

    params = Config.get_params()
    manager = HandleManager()
    manager.add_handlers(WantedHandler())
    manager.handle(params=params)


if __name__ == '__main__':
    main()
