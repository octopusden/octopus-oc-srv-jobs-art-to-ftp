import logging
from app import create_app
from config import Config
from sys import stderr

app = create_app(Config)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    stderr_handler = logging.StreamHandler(stderr)
    app.logger.addHandler(stderr_handler)

