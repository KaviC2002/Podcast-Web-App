import pytest
from podcast.search import services
from podcast.adapters import memory_repository, repository_populate
from podcast.adapters.memory_repository import MemoryRepository

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    repository_populate.populate(repo)
    return repo
@pytest.mark.parametrize(('query', 'filter_by', 'podcast_number'), (
        ('a', 'title', 812),
        ('Business', 'category', 87),
        ('Radio X', 'author', 1)))
def test_services_search_podcasts(in_memory_repo, query, filter_by, podcast_number):
    # check if the service layer can get the podcasts searched by title/category/author from the repository
    searched_podcasts = services.search_podcasts(in_memory_repo, query, filter_by)
    assert podcast_number == len(searched_podcasts)

