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
    session.add(ins_user)
    session.commit()

    # retrieve user
    retr_user = User.get(id=1)
    assert retr_user.id == 1, "test user id does not match"
    assert retr_user.name == "test_user", "test user name does not match"
    assert retr_user.is_bot is False, "test user bot status does not match"

def test_update(session):
    """update the user entry created before, and assert it has the new values"""

    # retrieve user
    upd_user = User.get(id=1)

    # update user
    upd_user.update(id=1, name="ralph", is_bot=True)

    # assert update is performed correctly
    retr_user = User.get(id=1)
    assert retr_user.name == "ralph", "test user name does not match"
    assert retr_user.is_bot is True, "test user bot status does not match"

def test_delete(session):
    """ deletes user entry created before and asserts thet it hast been deleted """

    # delete user
    User.delete(id=1)

    # assert no users are returned when querying for all users
    assert len(User.get_all()) == 0, "still user in DB, deletion not successful"

def test_create_multiple(session):
    """ create and retrieve multiple users """

    # create list of test users
    ins_users = (
        {"id": 1, "name": "Jens", "is_bot": False},
        {"id": 69, "name": "Rudolf", "is_bot": False},
        {"id": 307, "name": "Dieterbot", "is_bot": True}
    )

    # insert user object into db
    for user in ins_users:
        tmp = User(id=user["id"], name=user["name"], is_bot=user["is_bot"])
        tmp.save()

    # retrieve all users
    retr_users = User.get_all()

    for ins_user, retr_user in zip(ins_users, retr_users):
            assert ins_user["id"] == retr_user.id, f"id does not match for {ins_user}, {retr_user}"
            assert ins_user["name"] == retr_user.name, f"name does not match for {ins_user}, {retr_user}"
            assert ins_user["is_bot"] == retr_user.is_bot, f"bot status does not match for {ins_user}, {retr_user}"
    
# test cases for the sad path
def test_invalid_input(session):
    pass

def test_user_exists(session):
    # insert first user
    user_1 = User(id=111, name="Test User", is_bot=False) 
    
    # insert second user with same properties
    # should throw an integrity error
    user_2 = User(id=111, name="Test User", is_bot=False)
    assert sqlalchemy.exc.IntegrityError 

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