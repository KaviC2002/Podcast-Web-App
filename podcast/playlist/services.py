from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, User, Playlist, Episode


def add_to_playlist(repo, user_id, item_id):
    user = repo.get_user_by_id(user_id)
    print(user)
    if not user:
        raise ValueError("User not found")
    if user.playlist is None:
        playlist = Playlist(len(repo.get_playlists()) + 1, user, f"{user.username}'s playlist")
    else:
        playlist = repo.get_playlist_by_user(user_id)
    podcast = repo.get_podcast_by_id(item_id)
    playlist.add_podcast(podcast)
    user.set_playlist(playlist)
    repo.add_podcast_to_playlist(playlist, user_id, item_id)

def remove_from_playlist(repo, user_id, item_id):
    user = repo.get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")
    # get the user's playlist remove podcast from the playlist
    playlist = repo.get_playlist_by_user(user_id)
    podcast = repo.get_podcast_by_id(item_id)
    playlist.remove_podcast(podcast)
    # update the user's playlist
    user.set_playlist(playlist)
    # pass the updated playlist
    repo.remove_podcast_from_playlist(playlist, user_id, item_id)

def get_user_playlists(repo, user_id):
    user = repo.get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")
    playlist = repo.get_playlist_by_user(user_id)
    return playlist
