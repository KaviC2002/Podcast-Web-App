from flask import Blueprint, request, render_template
from .services import search_podcasts
import podcast.adapters.repository as repo
from podcast.search.services import get_searched_podcasts

search_blueprint = Blueprint('search_bp', __name__)
@search_blueprint.route('/search', methods=['GET'])
def search_results():
    if repo.repo_instance is None:
        raise ValueError("Repository instance is not initialized.")

    query = request.args.get('query')
    filter_by = request.args.get('filter')

    results = search_podcasts(repo.repo_instance, query, filter_by)

    page = request.args.get('page', 1, type=int)

    category_filter = request.args.get('category')
    author_filter = request.args.get('author')
    title_filter = request.args.get('title')
    per_page = 10

    podcasts, total_pages, prev_page, next_page, start_page, end_page = get_searched_podcasts(
        results, page, per_page, 10, category_filter, author_filter, title_filter)

    return render_template(
        'searchResults.html',
        filter_by = filter_by,
        query = query,
        results=podcasts,
        page=page,
        total_pages=total_pages,
        prev_page=prev_page,
        next_page=next_page,
        start_page=start_page,
        end_page=end_page
    )
