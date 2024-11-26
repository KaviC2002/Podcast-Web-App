import pytest

from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.domainmodel.model import User, Review, Podcast, Playlist
from podcast.adapters.repository import RepositoryException

# run db test with python -m pytest -v tests_db



def test_repository_can_add_a_user(session_factory):
    # test if a user is added to the database
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'Henry', '1234abcd')
    repo.add_user(user)

    assert len(repo.get_users()) == 1

def test_repository_can_add_a_review(session_factory):
    # test if a user can add a review to the database
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'Henry', '1234abcd')
    repo.add_user(user)

    # get a podcast by id from the database
    podcast = repo.get_podcast_by_id(1)
    print(podcast.title)
    print(podcast.id)

    review = Review(1, podcast, user, 5, "good")
    repo.add_review(review)

    assert len(repo.get_reviews()) == 1

def test_repository_playlist(session_factory):
    # test if a user can add a podcast to the playlist and remove a podcast from the playlist
    repo = SqlAlchemyRepository(session_factory)
    # create a user
    user = User(1, 'Henry', '1234abcd')
    # create a playlist for user
    playlist = Playlist(1, user, f"{user.username}'s playlist")
    # give the user the playlist, the user initially must have a playlist so playlist is in session
    user.set_playlist(playlist)
    # add the user to the repo
    repo.add_user(user)


    # get a podcast by id from the database
    podcast = repo.get_podcast_by_id(1)
    # add the podcast to the user's playlist
    playlist.add_podcast(podcast)
    user.set_playlist(playlist)
    repo.add_podcast_to_playlist(playlist, user.id, podcast.id)
    # get the user's playlist
    user_playlist = repo.get_playlist_by_user(user.id)

    assert len(repo.get_playlists()) == 1
    assert len(user_playlist.podcasts) == 1

    # remove the podcast from the user's playlist
    user_playlist.remove_podcast(podcast)
    user.set_playlist(user_playlist)
    repo.remove_podcast_from_playlist(user_playlist, user.id, podcast.id)
    # make sure the playlist is not removed but the podcast in the playlist is removed
    assert len(repo.get_playlists()) == 1
    assert len(user_playlist.podcasts) == 0

def test_repository_can_search_by_title(session_factory):
    # test if a repo search podcasts by title and return a list of searched podcasts
    repo = SqlAlchemyRepository(session_factory)

    # there are 2 podcasts with a title containing the word "around"
    # the 1st podcast should have a title of '#AroundThePoolTable'
    searched_podcasts = repo.search_by_title("around")
    searched_podcast = searched_podcasts[0]

    assert len(searched_podcasts) == 2
    assert searched_podcast.title == "#AroundThePoolTable"

def test_repository_can_search_by_category(session_factory):
    # test if a repo search podcasts by category and return a list of searched podcasts
    repo = SqlAlchemyRepository(session_factory)

    # there are 3 podcasts with a category "business"
    # the 1st podcast should have a title of 'The Packed Party Podcast'
    searched_podcasts = repo.search_by_category("shopping")
    searched_podcast = searched_podcasts[0]

    assert len(searched_podcasts) == 3
    assert searched_podcast.title == "The Packed Party Podcast"

def test_repository_can_search_by_author(session_factory):
    # test if a repo search podcasts by author and return a list of searched podcasts
    repo = SqlAlchemyRepository(session_factory)

    # there is 1 podcast with a author "radio x"
    # this podcast should have a title of 'The Chris Moyles Show on Radio X Podcast'
    searched_podcasts = repo.search_by_author("radio x")
    searched_podcast = searched_podcasts[0]

    assert len(searched_podcasts) == 1
    assert searched_podcast.title == "The Chris Moyles Show on Radio X Podcast"


