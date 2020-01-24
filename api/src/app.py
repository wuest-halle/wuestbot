import os

from flask import Flask, Blueprint, make_response
from flask_restful import Api
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

from log import Logger
from resources.healthz import Healthz

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')
Logger.LOG_LEVEL = LOG_LEVEL
LOGGER = Logger("root")


app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
app.config['OPENAPI_SPEC'] = "openapi/spec.yml"
blueprint = Blueprint('v1', __name__, url_prefix='/v1')
api = Api(blueprint)

if ENVIRONMENT == 'development':
    metrics = PrometheusMetrics(app)
else:
    metrics = GunicornInternalPrometheusMetrics(app)

@app.errorhandler(404)
@metrics.do_not_track()
def page_not_found(e):
    resp = make_response("Not found")
    resp.headers['Content-Type'] = "text/plain"
    resp.status_code = 404
    return resp

api.add_resource(Healthz, "/healthz")
app.register_blueprint(blueprint)

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(host="127.0.0.1", port=5000, debug=True)
