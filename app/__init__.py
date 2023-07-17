from logging import basicConfig, error, info, DEBUG
from flask import Flask, Blueprint
from os import environ
from app.art_to_ftp import ArtifactoryToFTP

basicConfig(level=DEBUG)

art_to_ftp_bp = Blueprint("art_to_ftp_bp", __name__)
from app.routes import *


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    if not app.config["TESTING"]:
        setup_art_to_ftp(app)
    app.register_blueprint(art_to_ftp_bp)
    return app

def setup_art_to_ftp(app):
    try:
        path = environ["PATH"]
    except KeyError as error_key:
        error("Missing env variables")
        exit(1)

    app.config["ART_TO_FTP"] = ArtifactoryToFTP()
    info("Artifactory to FTP is set up.")

