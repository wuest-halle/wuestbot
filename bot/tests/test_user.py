import os
from app.database.db_objects import User, db_name
from app.db_create import create_db

DB_NAME = os.path.abspath("tests/test-db.sqlite")

def setup_function():
    """Setting up the database."""
    os.environ['DB_NAME'] = DB_NAME
    create_db(db_name())

def test_user_create():
    assert True

def teardown_function():
    """Tearing down the database."""
    os.remove(db_name())