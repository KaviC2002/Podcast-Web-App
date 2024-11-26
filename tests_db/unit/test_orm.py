import pytest

import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

from podcast.domainmodel.model import User

# run db test with python -m pytest -v tests_db

def insert_user(empty_session, values=None):
    new_id = 1
    new_name = "henry"
    new_password = "1234abcd"

    if values is not None:
        new_id = values[0]
        new_name = values[1]
        new_password = values[2]

    empty_session.execute(text('INSERT INTO users (user_id, username, password) VALUES (:user_id, :username, :password)'),
                          {'user_id': new_id, 'username': new_name, 'password': new_password})
    row = empty_session.execute(text('SELECT user_id from users where user_id = :user_id'),
                                {'user_id': new_id}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute(text('INSERT INTO users (user_id, username, password) VALUES (:user_id, :username, :password)'),
                              {'user_id': value[0], 'username': value[1], 'password': value[2]})
    rows = list(empty_session.execute(text('SELECT user_id from users')).mappings().all())
    keys = tuple(row["user_id"] for row in rows)
    return keys

def make_user():
    user = User(1,"henry", "1234abcd")
    return user

def test_saving_of_users(empty_session):
    # check if a user is added to database using sql commands to check if the mapping is done correctly
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT user_id, username, password FROM users')))
    assert rows == [(1, "henry", "1234abcd")]

def test_loading_of_users(empty_session):
    # test if users can be loaded from the db
    users = list()
    users.append((1, "Andrew", "1234abcd"))
    users.append((2, "Cindy", "1111aaaa"))
    insert_users(empty_session, users)

    expected = [
        User(1,"Andrew", "1234abcd"),
        User(2,"Cindy", "1111aaaa")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users_with_common_user_id(empty_session):
    # test if the db doesn't allow the same user ids to be registered
    insert_user(empty_session, (1, "henry", "1234abcd"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(1,"henry", "1234abcd")
        empty_session.add(user)
        empty_session.commit()



