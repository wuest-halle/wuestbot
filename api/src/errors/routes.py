"""
This module collects all error handlers
"""

from flask import make_response

from src.errors import blueprint
from src import metrics

@blueprint.app_errorhandler(404)
@metrics.do_not_track()
def page_not_found(e):
    """ The 404 error handler """
    
    resp = make_response("Not found")
    resp.headers['Content-Type'] = "text/plain"
    resp.status_code = 404
    return resp