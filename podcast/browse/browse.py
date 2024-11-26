from flask import Blueprint, render_template, request  # Add request to handle query parameters
import podcast.adapters.repository as repo
from podcast.browse.services import get_podcasts

# Configure Blueprint catalogue
browse_blueprint = Blueprint(
    'browse_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse_podcasts():
    page = request.args.get('page', 1, type=int)
    category_filter = request.args.get('category')
    author_filter = request.args.get('author')
    title_filter = request.args.get('title')
    per_page = 10

    podcasts, total_pages, prev_page, next_page, start_page, end_page = get_podcasts(
        repo.repo_instance, page, per_page, 10, category_filter, author_filter, title_filter)


    return render_template(
        'catalogue.html',
        podcasts=podcasts,
        page=page,
        total_pages=total_pages,
        prev_page=prev_page,
        next_page=next_page,
        start_page=start_page,
        end_page=end_page
    )
