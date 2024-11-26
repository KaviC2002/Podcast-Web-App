from flask import Blueprint, render_template, request
import podcast.adapters.repository as repo
from podcast.home.services import get_podcast, get_pagination_podcasts

home_blueprint = Blueprint(
    'home_bp', __name__
)

@home_blueprint.route('/', methods=['GET'])
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 6

    podcasts, total_pages, prev_page, next_page, start_page, end_page = get_pagination_podcasts(
        repo.repo_instance, page, per_page)

    return render_template(
        'layout.html',
        podcasts=podcasts,
        page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        prev_page=prev_page,
        next_page=next_page
    )


