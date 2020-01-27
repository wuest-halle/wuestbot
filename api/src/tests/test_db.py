"""Provides classes to test different DB functionalities

TO DO:
    * test for User table (exists)
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

    def test_create(client):
        """Tests, if User object can be created and saved"""

        test_user = User(id=1, name="test_user", is_bot=False)
        assert test_user, "Creation of test user failed"
        with app.app_context():
            test_user.save()
    
    def test_get(client):
        """Tests, if a single user record can be retrieved"""
        
        with app.app_context():
            assert User.get(1), "Retrieval of user record failed"

    def test_update(client):
        """Tests, if a single User record can be updated"""
        id = 1
        name = "user_test"
        is_bot = True

        with app.app_context():
            User.update(id, name, is_bot)
            test_user = User.get(1)

        assert test_user.name == name, "Updating user's name failed"
        assert test_user.is_bot == is_bot, "updating users is_bot attribute failed"

    def test_get_all(client):
        """Tests, if all user records can be retrieved in a list"""

        with app.app_context():
            test_users = User.get_all()
        
        assert type(test_users) is list, "Return data type for getting all Users is not a list"

    def test_delete(client):
        """Tests, if a single user record can be deleted"""

        with app.app_context():
            User.delete(1)

        assert not User.get(1), "Deletion of user record failed"