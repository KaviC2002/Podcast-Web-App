from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast

def get_episode_by_id(repo, episode_id):
    return repo.get_episode_by_id(episode_id)


