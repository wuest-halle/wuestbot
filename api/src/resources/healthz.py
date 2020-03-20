from flask_restful import Resource
from flask import make_response

from src.log import Logger

LOGGER = Logger(__name__)

class Healthz(Resource):
    """Used to check health state"""

    def get(self):
        resp = make_response("OK")
        resp.headers['Content-Type'] = "text/plain"
        return resp
