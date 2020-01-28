"""Provides all fixtures for the testing framework

TO DO:
    * change to factory function for creation of test instance once written in app.py
    * add database fixture
    * add database session fixture (for scoped transactions in tests)
    * move override settings to file
    * set testing db to permanent file
    * write function for migrations once they're set up
"""
import os
import tempfile

import pytest
from flask import Flask

from app import app
from db import db

# provide testing settings in a dict
# this is probably being moved to a file later 
SETTINGS = {
    'ENV': 'testing',
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'OPENAPI_SPEC': 'openapi/spec.yml'
}


@pytest.fixture(scope="session")
def test_app(request):
    """Provides a single application instance to perform all tests on,
    which is going to be torn down after finishing. """

    # create testing instance
    test_app = app

    # bind database engine to testing app
    db.init_app(test_app)

    # override default settings with test settings 
    test_app.config.from_mapping(SETTINGS)

    # establish application context
    with test_app.app_context() as ctx:
        ctx.push()

    # Create a temporary prometheus_multiproc_dir
    # artefact from first fixture prototype, not sure yet if this is the right place 
    mpd_fd = tempfile.mkdtemp()
    os.environ['prometheus_multiproc_dir'] = mpd_fd

    # Teardown block after finishing tests
    def teardown():
        os.rmdir(mpd_fd)
        ctx.pop()
    
    request.addfinalizer(teardown)
    
    return test_app

@pytest.fixture(scope="session")
def client(test_app):
    """session-wide client"""

    with test_app.test_client() as client:
        yield client