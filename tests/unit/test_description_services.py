import pytest
from podcast.description import services
from podcast.authentication import services as auth_services


def test_services_get_podcast_by_id(in_memory_repo):
    # test if the browse service layer can get all the podcasts from the repository
    podcast1 = services.get_podcast_by_id(in_memory_repo, 1)
    assert podcast1.title == "D-Hour Radio Network"

def test_services_episode_pagination(in_memory_repo):
    # test if the episode pagination works
    episodes, total_pages, prev_page, next_page, start_page, end_page = services.get_paginated_episodes(in_memory_repo,
    872, 1, 8)
    # this podcast only has 4 episodes which is less than the limited number of episodes per page, 8
    # so the total pages, starting page and ending page are all 1
    # previous page and next page don't exist
    assert len(episodes) == 4
    assert total_pages == 1
    assert prev_page == None
    assert next_page == None
    assert start_page == 1
    assert end_page == 1

def test_services_add_review(in_memory_repo):
    # test if the service layer can add a review to the repository
    auth_services.add_user('henry', '1234abcd', in_memory_repo)
    services.add_review(in_memory_repo, 5, 'good', 5, 'henry')
    assert len(in_memory_repo.get_reviews()) == 1



