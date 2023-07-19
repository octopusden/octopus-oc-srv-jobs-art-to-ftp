import io
import flask
import logging
from oc_cdtapi import NexusAPI
from ftplib import FTP
import os
from . import art_to_ftp_bp

logging.basicConfig(level=logging.DEBUG)

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
    logging.debug('Initializing NexusAPI')
    na = NexusAPI.NexusAPI()
    logging.debug('Checking existence of [%s]' % gav)
    if not na.exists(gav):
        logging.error('Source artifact was not found')
        return response(404, '{"result": "Source artifact not found"}')
    logging.debug('Artifact exisits, downloading')
    data = na.cat(gav, binary=True)
    logging.debug('Downloaded [%s] bytes' % len(data))
    fd = io.BytesIO(data)
    ftp_host = os.getenv('FTP_URL')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASSWORD')
    logging.debug('Opening ftp connection to [%s] at [%s]' % (ftp_host, ftp_user))
    ftp = FTP(ftp_host, ftp_user, ftp_pass)
    ftpcmd = 'STOR %s' % target_path
    logging.debug('Trying to store file to [%s]' % target_path)
    try:
        retmsg = ftp.storbinary(ftpcmd, fd)
    except:
        return response(500, '{"result": "error", "message": "%s"}' % retmsg)
    logging.debug('FTP server responded with [%s]' % retmsg)
    return response(200, '{"result": "ok"}')

