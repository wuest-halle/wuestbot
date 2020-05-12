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
    """ test for faulty input, such as lacking arguments, wrong type of arguments """
    
    user_1 = User(id=1)
    user_1.save()

    user_2 = User(id=2, name=111, is_bot=22)
    user_2.save()
    
    with pytest.raises(Exception) as e:
        User.get(id=1)
        User.get(id=2)
        print("Invalid data cannot be entered:", e)


def test_user_exists(session):
    """ test for integrity constraints (double input of unique ID) """

    # insert first user
    user_1 = User(id=111, name="Test User", is_bot=False) 
    
    # insert second user with same properties
    # should throw an integrity error
    user_2 = User(id=111, name="Test User", is_bot=False)
    assert sqlalchemy.exc.IntegrityError 
