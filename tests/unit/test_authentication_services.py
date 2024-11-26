import pytest
from podcast.authentication import services

def test_services_add_user(in_memory_repo):
    # test if the service layer can add an user to the repository
    services.add_user('henry', '1234abcd', in_memory_repo)
    assert len(in_memory_repo.get_users()) == 1

def test_get_user(in_memory_repo):
    # test if the service layer can get an user from the repository while converting it into a dictionary form
    services.add_user('henry', '1234abcd', in_memory_repo)
    user = services.get_user('henry', in_memory_repo)
    # check if the dictionary contains the added user information
    # check if the username is stored
    assert user.username == 'henry'
    # check if the password is encrypted and stored successfully for security
    assert user.password != '1234abcd'



