from flask import Blueprint, render_template, redirect, url_for
import podcast.adapters.repository as repo
from podcast.description.episodes.services import get_episode_by_id

episode_blueprint = Blueprint(
    'episode_bp', __name__)

@episode_blueprint.route('/episode_description/<int:episode_id>', methods=['GET'])
def show_episode_description(episode_id):
    episode = get_episode_by_id(repo.repo_instance, episode_id)
    if episode is None:
        return redirect(url_for('home_bp.home'))
    return render_template('episodeDescription.html', episode=episode)