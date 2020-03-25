"""Provides classes to test different DB functionalities
"""

import pytest
import sqlalchemy

from src import db
from models.users import User

# test cases for the happy path
def test_create(session):
    """Tests the creation and retrieval of a single user"""

    # create user object
    ins_user = User(id=1, name="test_user", is_bot=False)
    assert ins_user.id == 1, "test user's id does not match"
    assert ins_user.name == "test_user", "test user's name does not match"
    assert ins_user.is_bot is False, "test user's bot status does not match"

    # insert into database
    assert ins_user.save() is not sqlalchemy.exc.SQLAlchemyError, "SQLAlchemy Exception was thrown"

    # retrieve user
    retr_user = User.get(id=1)
    assert retr_user.id == 1, "test user id does not match"
    assert retr_user.name == "test_user", "test user name does not match"
    assert retr_user.is_bot is False, "test user is bot, but should not be"

def test_update():
    pass

def test_delete():
    pass

def test_create_multiple():
    pass

# test cases for the sad path


#class TestUser():
#
#    def test_table_exists(database):
#        """Tests, if table Users is existing"""
#
#        print(db.engine)
#
#        assert "Users" in db.metadata.tables, "Table 'Users' does not exist"
#
#    def test_create(database):
#        """Tests, if User object can be created and saved"""
#
#        test_user = User(id=1, name="test_user", is_bot=False)
#        assert test_user, "Creation of test user Object failed"
#       
#        test_user.save()
#    
#    def test_get(database):
#        """Tests, if a single user record can be retrieved"""
#        
#        assert User.get(1), "Retrieval of user record failed"
#
#    def test_update(database):
#        """Tests, if a single User record can be updated"""
#        id = 1
#        name = "user_test"
#        is_bot = True
#  
#        User.update(id, name, is_bot)
#        test_user = User.get(1)
#
#        assert test_user.name == name, "Updating user's name failed"
#        assert test_user.is_bot == is_bot, "updating users is_bot attribute failed"
#
#    def test_get_all(database):
#        """Tests, if all user records can be retrieved in a list"""
#       
#        test_users = User.get_all()
#        
#        assert type(test_users) is list, "Return data type for getting all Users is not a list"
#
#    def test_delete(database):
#        """Tests, if a single user record can be deleted"""
#
#        User.delete(1)
#        assert User.get(1) is None, "Deletion of user record failed"
#