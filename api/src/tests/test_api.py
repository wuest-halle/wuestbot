import pytest
import os
import tempfile

from yaml import safe_load

from flask import request
from openapi_core import create_spec
from openapi_core.shortcuts import ResponseValidator
from openapi_core.wrappers.flask import FlaskOpenAPIResponse, FlaskOpenAPIRequest

from app import app

@pytest.fixture
def client():
    # Allow exceptions to propagate
    app.config['TESTING'] = True

    # Create a temporary sqlite3 database
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()

    # Create a temporary prometheus_multiproc_dir
    mpd_fd = tempfile.mkdtemp()
    os.environ['prometheus_multiproc_dir'] = mpd_fd

    with app.test_client() as client:
        yield client

    # Cleanup the temporary database and folder
    os.close(db_fd)
    os.rmdir(mpd_fd)
    os.unlink(app.config['DATABASE'])

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

