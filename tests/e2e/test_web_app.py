import pytest

from flask import session

import pytest

from podcast import create_app
from podcast.adapters import memory_repository, repository_populate
from podcast.adapters.memory_repository import MemoryRepository
from podcast.authentication import services as auth_service

from utils import get_project_root

# the csv files in the test folder are different from the csv files in the podcast/adapters/data folder!
# tests are written against the csv files in tests, this data path is used to override default path for testing
TEST_DATA_PATH = get_project_root() / "tests" / "data"
@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    repository_populate.populate(repo)
    return repo

@pytest.fixture(scope='session')
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def register(self, user_name='thorke', password='1234abcd'):
        return self.__client.post(
            'authentication/register',
            data={'user_name': user_name, 'password': password}
        )

    def login(self, user_name='thorke', password='1234abcd'):
        return self.__client.post(
            'authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain a lower case letter and a digit')

))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data

def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    # In the covid web app, some users are already loaded to the repository from the csv file but for this assignment,
    # we have no users in the repository so we have to register an user first before the log in.
    response = auth.register()
    response = auth.login()
    assert response.headers['Location'] == '/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'thorke'

def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200


def test_review(client, auth):
    # Register and Login a user.
    auth.register()
    auth.login()

    # Check that we are redirected to the podcast description page after reviewing that podcast
    response = client.post(
        '/submit_review/1',
        data={'rating': 5, 'comment': 'good'}
    )
    assert response.headers['Location'] == '/description/1'

