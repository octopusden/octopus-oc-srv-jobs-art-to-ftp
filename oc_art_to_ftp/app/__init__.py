from flask import Flask, Blueprint
from oc_logging.Logging import setup_logging

art_to_ftp_bp = Blueprint("art_to_ftp_bp", __name__)
from .routes import *


def create_app(config_class):
    setup_logging()
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(art_to_ftp_bp)
    return app
