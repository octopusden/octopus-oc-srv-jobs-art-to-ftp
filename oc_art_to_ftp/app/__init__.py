from flask import Flask, Blueprint

art_to_ftp_bp = Blueprint("art_to_ftp_bp", __name__)
from .routes import *


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(art_to_ftp_bp)
    return app
