import pytest

from podcast.domainmodel.model import Podcast, Author, Episode, Review, User
from podcast.adapters.repository import RepositoryException
from podcast.adapters import memory_repository, repository_populate
from podcast.adapters.memory_repository import MemoryRepository

@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")

@pytest.fixture
def my_podcast(my_author):
    return Podcast(1, my_author, "Amazing podcast")

@pytest.fixture
def my_episode(my_podcast):
    return Episode(1, my_podcast, "first episode   " )
@pytest.fixture
def my_user():
    return User(1, "Henry", "1234abcd")
@pytest.fixture
def my_review(my_podcast, my_user):
    return Review(1, my_podcast, my_user, 5, "good")

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    repository_populate.populate(repo)
    return repo
def test_repository_can_search_by_title(in_memory_repo):
    # get all the podcasts that contain the letter "a" in the title
    a_podcasts = in_memory_repo.search_by_title('a')
    # test if the number of podcasts is correct
    assert len(a_podcasts) == 812
def test_repository_can_search_by_category(in_memory_repo):
    # get all the podcasts categorized to business
    business_podcasts = in_memory_repo.search_by_category('Business')
    # test if the number of podcasts is correct
    assert len(business_podcasts) == 87

def test_repository_can_search_by_author(in_memory_repo):
    # get all the podcasts published by the author 'Radio X'
    podcasts_by_Radio_X = in_memory_repo.search_by_title('Radio X')
    # test if the number of podcasts is correct
    assert len(podcasts_by_Radio_X) == 1


def test_repository_can_retrieve_podcast_count(in_memory_repo):
    number_of_podcasts = in_memory_repo.get_number_of_podcasts()
    # Check that the query returned 982 Podcasts excluding invalid ones
    assert number_of_podcasts == 982

def test_repository_can_retrieve_episode_count(in_memory_repo):
    number_of_episodes = in_memory_repo.get_number_of_episodes()
    # Check that the query returned 5370 Episodes excluding invalid ones
    assert number_of_episodes == 5370

def test_repository_can_retreive_podcast_by_id(in_memory_repo):
    # check that the episode with an id of 1 is returned
    podcast1 = in_memory_repo.get_podcast_by_id(1)
    assert podcast1.title == "D-Hour Radio Network"

def test_repository_can_retreive_episode_by_id(in_memory_repo):
    # check that the episode with an id of 1 is returned
    episode1 = in_memory_repo.get_episode_by_id(1)
    assert episode1.title == "The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3"

def test_repository_can_add_podcast(in_memory_repo, my_podcast):
    # check that a podcast is added so the number of podcasts is increased by 1
    in_memory_repo.add_podcast(my_podcast)
    assert in_memory_repo.get_number_of_podcasts() == 983

def test_repository_can_add_episode(in_memory_repo, my_episode):
    # check that a episode is added so the number of episodes is increased by 1
    in_memory_repo.add_episode(my_episode)
    assert in_memory_repo.get_number_of_episodes() == 5371

def test_repository_can_add_review(in_memory_repo, my_review):
    # check that a review is added to the repository so the number of reviews is increased by 1
    in_memory_repo.add_review(my_review)
    assert len(in_memory_repo.get_reviews()) == 1

def test_repository_can_add_user(in_memory_repo, my_user):
    # check that an user is added to the repository so the number of users is increased by 1
    in_memory_repo.add_user(my_user)
    assert len(in_memory_repo.get_users()) == 1


