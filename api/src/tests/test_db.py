"""Provides classes to test different DB functionalities

TO DO:
    * test for User table (empty)
    * test creation and insertion of User object
    * test update of User object
    * test list return of all Users
    * test deletion of User record
"""

import pytest

from app import app
from db import db
from models.users import User

class TestUser():

    def test_table_exists(client):
        """Tests, if table Users is existing"""

        assert "Users" in db.metadata.tables, "Table 'Users' does not exist"



