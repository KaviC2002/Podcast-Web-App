import abc
from typing import List

from podcast.domainmodel.model import Podcast, Episode, User, Review, Playlist, Author, Category

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'Repository exception: {message}')


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name: str) -> User:
        raise NotImplementedError
    @abc.abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        raise NotImplementedError


    @abc.abstractmethod
    def get_users(self) -> List[User]:
        raise NotImplementedError
    @abc.abstractmethod
    def add_podcast(self, podcast: Podcast):
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_podcasts(self, podcasts: List[Podcast]):
        """ Add multiple podcasts to the repository of podcast. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts(self) -> List[Podcast]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_podcasts(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast_by_id(self, podcast_id: int) -> Podcast:
        raise NotImplementedError

    @abc.abstractmethod
    def add_episode(self, episode: Episode):
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_episodes(self, episodes: List[Episode]):
        """ Add multiple episodes to the repository of episode. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes(self) -> List[Episode]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_episodes(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_episode_by_id(self, episode_id: int) -> Episode:
        raise NotImplementedError


    @abc.abstractmethod
    def add_review(self, review: Review):
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.podcast is None or review not in review.podcast.reviews:
            raise RepositoryException('Review not correctly attached to an Podcast')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_categories(self, categories: List[Category]):
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_authors(self, authors: List[Author]):
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_title(self, title):
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_category(self, category):
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_author(self, author):
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlists(self):
        raise NotImplementedError
    @abc.abstractmethod
    def get_playlist_by_user(self, user_id):
        raise NotImplementedError
    @abc.abstractmethod
    def add_podcast_to_playlist(self, playlist, user_id: int, podcast_id: int):
        """Add a podcast to the user's playlist."""
        raise NotImplementedError

    @abc.abstractmethod
    def remove_podcast_from_playlist(self, playlist, podcast_id: int, user_id: int):
        """Remove a podcast from the user's playlist."""
        raise NotImplementedError

