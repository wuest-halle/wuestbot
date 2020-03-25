"""Provides all fixtures for the testing framework
"""
import os
import tempfile

import pytest
from flask import Flask

from src import create_app, db

# provide testing settings in a dict
# this is probably being moved to a file later 

@pytest.fixture(scope="session")
def test_app(request):
    """Provides a single application instance to perform all tests on,
    which is going to be torn down after finishing. """

    # create testing instance
    test_app = create_app()

    # establish application context
    ctx = test_app.app_context()
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
def database(test_app, request):
    """Test database to perform all ops on, cleaned after tests have been finished"""

    # Create all tables
    db.create_all()

    return db

    db.drop_all()

@pytest.fixture(scope="function")
def session(test_app, database):
    """Creates a scoped session for every test"""
    conn = db.engine.connect()
    trans = conn.begin()

    session = db.create_scoped_session()

    db.session = session

    yield session

    trans.rollback()
    conn.close()
    session.remove()


@pytest.fixture(scope="session")
def client(test_app):
    """session-wide client"""

    with test_app.test_client() as client:
        yield client