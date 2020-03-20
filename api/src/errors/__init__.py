"""
This package collects all error handling related routes and messages. They are 
connected to the app instance via a blueprint.
"""

from flask import Blueprint

blueprint = Blueprint('errors', __name__)

from src.errors import routes