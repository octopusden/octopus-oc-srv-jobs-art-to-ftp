from app import art_to_ftp_bp
from flask import Response, current_app, request
import json

def response(code, data):
    return Response(
        status=code,
        mimetype='application/json',
        response=data
    )

