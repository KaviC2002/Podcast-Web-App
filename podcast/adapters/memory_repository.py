from bisect import insort_left
from typing import List

from podcast.adapters.repository import AbstractRepository, RepositoryException
from podcast.domainmodel.model import Podcast, Episode, User, Review, Playlist, Author, Category


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__podcast = []
        self.__episode = []
        self.__users = []
        self.__reviews = []
        self.__playlists = []
        self.__categories = []
        self.__authors = []

    def add_multiple_categories(self, categories: List[Category]):
        for category in categories:
            insort_left(self.__categories, category)

    def add_multiple_authors(self, authors: List[Author]):
        for author in authors:
            insort_left(self.__authors, author)

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username: str) -> User:
        return next((user for user in self.__users if user.username == username), None)

    def get_user_by_id(self, user_id: int) -> User:
        print(f"Retrieving user with ID: {user_id}")
        user = next((user for user in self.__users if user.id == user_id), None)
        if user is None:
            print(f"User with ID {user_id} not found!")
        return user

    def get_users(self) -> List[User]:
        return self.__users

    def add_podcast(self, podcast: Podcast):
        if isinstance(podcast, Podcast):
            insort_left(self.__podcast, podcast)

    def add_multiple_podcasts(self, podcasts: List[Podcast]):
        for podcast in podcasts:
            insort_left(self.__podcast, podcast)

    def get_podcasts(self) -> List[Podcast]:
        return self.__podcast

    def get_number_of_podcasts(self):
        return len(self.__podcast)

    def get_podcast_by_id(self, podcast_id):
        print(f"Searching for podcast with ID: {podcast_id}")
        print(f"Available podcasts: {self.__podcast}")
        return next((podcast for podcast in self.__podcast if podcast.id == podcast_id), None)

    def add_episode(self, episode: Episode):
        if isinstance(episode, Episode):
            insort_left(self.__episode, episode)

    def add_multiple_episodes(self, episodes: List[Episode]):
        for episode in episodes:
            insort_left(self.__episode, episode)


    def get_episodes(self) -> List[Episode]:
        return self.__episode

    def get_number_of_episodes(self):
        return len(self.__episode)

    def get_episode_by_id(self, episode_id):
        for episode in self.__episode:
            if episode.id == episode_id:
                return episode
        return None  # If no matching podcast is found

    def add_review(self, review: Review):
        for i in range(len(self.__podcast)):
            if self.__podcast[i] == review.podcast:
                insort_left(self.__podcast[i].reviews, review)
        for i in range(len(self.__users)):
            if self.__users[i] == review.user:
                insort_left(self.__users[i].reviews, review)
        insort_left(self.__reviews, review)

    def get_reviews(self):
        return self.__reviews

    def search_by_title(self, title: str) -> List[Podcast]:
        return [podcast for podcast in self.__podcast if title.lower() in podcast.title.lower()]

    def search_by_category(self, category_name: str) -> List[Podcast]:
        return [podcast for podcast in self.__podcast if
                any(category.name.lower() == category_name.lower() for category in podcast.categories)]

    def search_by_author(self, author_name: str) -> List[Podcast]:
        return [podcast for podcast in self.__podcast if podcast.author.name.lower() == author_name.lower()]

    def get_playlists(self) -> List[Playlist]:
        return self.__playlists
    def get_playlist_by_user(self, user_id):
        user = self.get_user_by_id(user_id)
        return user.playlist
    def add_podcast_to_playlist(self, playlist, user_id, podcast_id):
        user = self.get_user_by_id(user_id)
        podcast = self.get_podcast_by_id(podcast_id)
        # if user has no playlist create one
        if user.playlist is None:
            user.set_playlist(playlist)
        # add the podcast to the user's playlist
        user.playlist.add_podcast(podcast)
        # add the playlist to the repository
        if user.playlist in self.__playlists:
            i = self.__playlists.index(user.playlist)
            self.__playlists[i] = user.playlist
        else:
            self.__playlists.append(user.playlist)

    def remove_podcast_from_playlist(self, playlist, user_id: int, podcast_id):
        user = self.get_user_by_id(user_id)
        # if the user has a playlist, remove the podcast from it
        if user.playlist:
            # find the index of the playlist in the repository first then remove it from the repository
            i = self.__playlists.index(user.playlist)
            self.__playlists[i] = user.playlist

