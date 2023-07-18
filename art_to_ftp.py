import flask
import logging
from oc_cdtapi import NexusAPI

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


@app.route('/ping', methods=['GET'])
def ping():
    logging.debug('Reached ping')
    return response(200, '{"result": "ok"}')


@app.route('/gav_copy', methods=['POST'])
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
    return response(200, '{"result": "ok"}')

