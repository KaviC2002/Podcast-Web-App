from abc import ABC
from typing import List, Type

from sqlalchemy import func
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist


# feature 1 test
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_multiple_authors(self, authors: List[Author]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for author in authors:
                    if author.name is None:
                        raise ValueError("Author name cannot be None")
                    scm.session.add(author)
            scm.commit()


    def add_multiple_categories(self, categories: List[Category]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for category in categories:
                    scm.session.add(category)
            scm.commit()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._username == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return user

    def get_user_by_id(self, user_id: int) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._id == user_id).one()
        except NoResultFound:
            print(f'user {user_id} was not found')
        return user

    def get_users(self) -> List[User]:
        users = self._session_cm.session.query(User).all()
        return users

    def get_podcasts(self, sorting: bool = False) -> List[Podcast]:
        podcasts = self._session_cm.session.query(Podcast).all()
        return podcasts

    def get_podcast_by_id(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            query = self._session_cm.session.query(Podcast).filter(
                Podcast._id == podcast_id)
            podcast = query.one()
        except NoResultFound:
            print(f'Podcast {podcast_id} was not found')

        return podcast

    def add_podcast(self, podcast: Podcast):
        with self._session_cm as scm:
            scm.session.merge(podcast)
            scm.commit()

    def add_multiple_podcasts(self, podcasts: List[Podcast]):
        with self._session_cm as scm:
            for podcast in podcasts:
                scm.session.add(podcast)
            scm.commit()

    def get_number_of_podcasts(self) -> int:
        num_podcasts = self._session_cm.session.query(Podcast).count()
        return num_podcasts

    def get_episodes(self, sorting: bool = False) -> list[Type[Episode]]:
        episodes = self._session_cm.session.query(Episode).all()
        return episodes

    def get_episode_by_id(self, episode_id: int) -> Episode:
        episode = None
        try:
            query = self._session_cm.session.query(Episode).filter(
                Episode._Episode__id == episode_id)
            episode = query.one()
        except NoResultFound:
            print(f'Podcast {episode_id} was not found')
        return episode

    def add_episode(self, episode: Episode):
        with self._session_cm as scm:
            scm.session.merge(episode)
            scm.commit()

    def add_multiple_episodes(self, episodes: List[Episode]):
        with self._session_cm as scm:
            for episode in episodes:
                scm.session.merge(episode)
            scm.commit()

    def get_number_of_episodes(self):
        num_episodes = self._session_cm.session.query(Episode).count()
        return num_episodes

    def get_reviews(self):
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def search_by_title(self, title: str) -> List[Podcast]:
        searched_podcasts = []
        try:
            searched_podcasts = self._session_cm.session.query(Podcast).filter(
                func.lower(Podcast._title).like(f"%{title}%")
            ).all()
        except NoResultFound:
            print(f'Podcasts with title {title} were not found')
        return searched_podcasts

    def search_by_category(self, category_name: str) -> List[Podcast]:
        searched_podcasts = []
        try:
            searched_podcasts = self._session_cm.session.query(Podcast). \
                filter(
                Podcast.categories.any(Category._name.like(f"%{category_name}%"))).all()
        except NoResultFound:
            print(f'Podcasts with category {category_name} were not found')
        return searched_podcasts


    def search_by_author(self, author_name: str) -> List[Podcast]:
        searched_podcasts = []
        try:
            searched_podcasts = self._session_cm.session.query(Podcast).join(Author). \
                filter(Author._name.like(f"%{author_name}%")).all()
        except NoResultFound:
            print(f'Podcasts with author {author_name} were not found')
        return searched_podcasts

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_playlists(self):
        # used to give unique id's for playlist objects
        playlists = self._session_cm.session.query(Playlist).all()
        return playlists

    def get_playlist_by_user(self, user_id):
        # use first() to return None when nothing's there
        query = self._session_cm.session.query(Playlist).join(User).filter(
                User._id == user_id)
        playlist = query.first()
        return playlist

    def add_podcast_to_playlist(self, playlist, user_id: int, podcast_id: int):
        with self._session_cm as scm:
            scm.session.merge(playlist)
            scm.commit()


    def remove_podcast_from_playlist(self, playlist, user_id: int, podcast_id):
        # after removing the podcast from the playlist, merge that playlist
        with self._session_cm as scm:
            scm.session.merge(playlist)
            scm.commit()





