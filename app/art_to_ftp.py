from requests import get, put
from requests.exceptions import ConnectionError
from urllib.parse import urljoin
from logging import info, error, debug, exception
import json, posixpath

class ArtifactoryToFTP:

    def __init__(self):
        """
        """
        None
