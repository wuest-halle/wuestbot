import os

from flask import Flask, Blueprint, make_response
from flask_restful import Api
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

from log import Logger
from resources.healthz import Healthz

from db import db
from models.users import User 

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')
Logger.LOG_LEVEL = LOG_LEVEL
LOGGER = Logger("root")
DATABASE_DIR = os.getenv('DATABASE_DIR')


app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
app.config['OPENAPI_SPEC'] = "openapi/spec.yml"
blueprint = Blueprint('v1', __name__, url_prefix='/v1')
api = Api(blueprint)

if ENVIRONMENT == 'development':
    metrics = PrometheusMetrics(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    metrics = GunicornInternalPrometheusMetrics(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_DIR or os.path('data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.errorhandler(404)
@metrics.do_not_track()
def page_not_found(e):
    resp = make_response("Not found")
    resp.headers['Content-Type'] = "text/plain"
    resp.status_code = 404
    return resp

api.add_resource(Healthz, "/healthz")
app.register_blueprint(blueprint)

@app.before_first_request
def create_tables():
    
    # create all tables on app startup
    db.create_all()
    
    # commit them, so they are saved and visible to the app
    db.session.commit()

db.init_app(app)

@app.shell_context_processor
def shell_context():
    """Creates the context for the `flask shell` command

    This function passes a dictionary back to the shell_context_processor 
    decorator function. The dict contains objects from the app and provides 
    them to the interpreter. This is useful for quick iteration testing 
    of new code without starting a new development instance
    """
    create_tables()
    return {'db': db, 'User': User}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
