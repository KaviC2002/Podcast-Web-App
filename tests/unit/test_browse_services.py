import pytest
from podcast.browse import services
def test_services_get_podcasts_number(in_memory_repo):
    # test if the browse service layer can get the number of podcasts from the repository
    podcasts = services.get_number_of_podcast(in_memory_repo)
    assert podcasts == 982

def test_services_podcast_pagination(in_memory_repo):
    # test if the podcast pagination works
    podcasts, total_pages, prev_page, next_page, start_page, end_page = services.get_podcasts(in_memory_repo, 1, 6)
    assert len(podcasts) == 6
    assert total_pages == 164
    # since it's the 1st page, there is no previous page.
    assert prev_page == None
    assert next_page == 2
    assert start_page == 1
    assert end_page == 10
