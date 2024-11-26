import pytest
from podcast.description.episodes import services

def test_services_get_episode_by_id(in_memory_repo):
    episode1 = services.get_episode_by_id(in_memory_repo, 1)
    assert episode1.title == "The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3"

