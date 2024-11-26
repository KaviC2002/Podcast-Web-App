from flask import Blueprint, request, session, redirect, url_for, render_template
import podcast.adapters.repository as repo
from .services import add_to_playlist, remove_from_playlist, get_user_playlists
from podcast.authentication.authentication import login_required


playlist_blueprint = Blueprint('playlist_bp', __name__)


@playlist_blueprint.route('/add_to_playlist', methods=['POST'])
@login_required
def add_to_playlist_route():
    user_id = session.get('user_id')
    podcast_id = request.form.get('podcast_id', type=int)  # Ensure it's converted to int
    add_to_playlist(repo.repo_instance, user_id, podcast_id)
    return redirect(url_for('playlist_bp.show_playlists'))


@playlist_blueprint.route('/remove_from_playlist', methods=['POST'])
@login_required
def remove_from_playlist_route():
    user_id = session.get('user_id')
    podcast_id = request.form.get('podcast_id', type=int)
    remove_from_playlist(repo.repo_instance, user_id, podcast_id)
    return redirect(url_for('playlist_bp.show_playlists'))

@playlist_blueprint.route('/my_playlists', methods=['GET'])
@login_required
def show_playlists():
    user_id = session.get('user_id')
    playlists = get_user_playlists(repo.repo_instance, user_id)
    return render_template('podcastplaylist.html', playlists=playlists)