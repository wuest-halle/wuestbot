"""
This is the app's main module used to initialize global objects which can then 
be used by the subsystems. It uses Flask's app Factory pattern for quick 
configuration in different scenarios, i.e. tests
"""
import os

from flask import Flask, Blueprint
from flask_restful import Api
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
from flask_sqlalchemy import SQLAlchemy


from src.log import Logger
from src.resources.healthz import Healthz

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')
Logger.LOG_LEVEL = LOG_LEVEL
LOGGER = Logger("root")

# create extension instances
db = SQLAlchemy()
api = Api()

if ENVIRONMENT == 'development':
    metrics = PrometheusMetrics(app=None)
else:
    metrics = GunicornInternalPrometheusMetrics(app=None)

blueprint = Blueprint('v1', __name__, url_prefix='/v1')

def create_app():
    """Factory method, creates app instance

    Arguments:
        * none

    Returns:
        * application instance
    """
    # create app instance and configure it from file
    app = Flask(__name__)
    app.config.from_envvar('CONFFILE')

    # initialize extensions
    db.init_app(app)
    metrics.init_app(app)
    api.init_app(blueprint)

    with app.app_context() as ctx:
        db.create_all()

    # register flask-restful's API endpoints
    api.add_resource(Healthz, "/healthz")

    # import the errors subsystem incl all error handlers here via its blueprint
    from src.errors import blueprint as errors_bp
    app.register_blueprint(errors_bp) 

    app.register_blueprint(blueprint) 
    
    return app


"""
LEGACY CODE - REVIEW AND INTEGRATE
from models.users import User 


if ENVIRONMENT == 'development':
    metrics = PrometheusMetrics(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    metrics = GunicornInternalPrometheusMetrics(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_DIR or os.path('data.db')
"""