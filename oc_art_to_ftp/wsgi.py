import logging
from .app import create_app
from .config import Config

app = create_app(Config)

# additional tricks for logging
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=gunicorn_logger.level)
