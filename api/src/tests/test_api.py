"""Provides all tests for API-related functions"""

from yaml import safe_load

from flask import request
from openapi_core import create_spec
from openapi_core.shortcuts import ResponseValidator
from openapi_core.wrappers.flask import FlaskOpenAPIResponse, FlaskOpenAPIRequest

def test_healthz(client):
    """Test the /healthz endpoint."""

    path = '/v1/healthz'
    rv = client.get(path)

    # Validate request and response against OpenAPI spec
    with app.test_request_context(path):
        with open(app.config['OPENAPI_SPEC']) as stream:
            spec = create_spec(safe_load(stream))

        openapi_response = FlaskOpenAPIResponse(rv)
        openapi_request = FlaskOpenAPIRequest(request)
        validator = ResponseValidator(spec)
        result = validator.validate(openapi_request, openapi_response)
        result.raise_for_errors()

    assert rv.content_type == "text/plain"
    assert rv.status_code == 200
    assert b'OK' in rv.data

def test_404(client):
    """Test custom 404 handler."""

    rv = client.get('/foo')
    assert rv.content_type == "text/plain"
    assert rv.status_code == 404
    assert b'Not found' in rv.data

