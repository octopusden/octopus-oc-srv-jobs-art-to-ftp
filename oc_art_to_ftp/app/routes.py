import flask
import logging
from . import art_to_ftp_bp
from .art_to_ftp import ArtToFTP

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(filename)s %(funcName)s %(message)s')

app = flask.Flask(__name__)

def response(code, data):
    logging.debug('Reached respose')
    logging.debug('code = [%s]' % code)
    logging.debug('data = [%s]' % data)
    return flask.Response(
        status=code,
        mimetype='application/json',
        response=data
    )


@art_to_ftp_bp.route('/ping', methods=['GET'])
def ping():
    logging.debug('Reached ping')
    return response(200, '{"result": "ok"}')


@art_to_ftp_bp.route('/gav_copy', methods=['POST'])
def gav_copy():
    logging.debug('Reached gav_copy')
    data = flask.request.json
    gav = data['gav']
    target_path = data['target_path']
    logging.debug('gav: [%s]' % gav)
    logging.debug('target_path: [%s]' % target_path)
    atf = ArtToFTP()
    resp_code, resp_msg = atf.gav_copy(gav, target_path)
    return response(resp_code, resp_msg)

@art_to_ftp_bp.route('/sync', methods=['POST'])
def sync():
    logging.debug('Reached sync')
    data = flask.request.json
    source_repo = data['source_repo']
    mask = data.get('mask')
    atf = ArtToFTP()
    resp_code, resp_msg = atf.sync(source_repo, mask)
    return response(resp_code, resp_msg)
