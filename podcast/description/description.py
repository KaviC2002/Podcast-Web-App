from flask import Blueprint, render_template, redirect, url_for, request, session
import podcast.adapters.repository as repo
from podcast.description.services import get_podcast_by_id, get_paginated_episodes, add_review
import podcast.description.services as services


from podcast.authentication.authentication import login_required


description_blueprint = Blueprint(
    'description_bp', __name__)


@description_blueprint.route('/description/<int:podcast_id>', methods=['GET'])
def show_podcast_description(podcast_id):
    podcast = get_podcast_by_id(repo.repo_instance, podcast_id)

    # Fetch all reviews and calculate the average rating
    reviews = sorted(podcast.reviews, key=lambda x: x.timestamp, reverse=True)
    if reviews:
        average_rating = round(sum([r.rating for r in reviews]) / len(reviews), 1)
    else:
        average_rating = None

    # Pagination for episodes
    page = request.args.get('page', 1, type=int)
    per_page = 6
    episodes, total_pages, prev_page, next_page, start_page, end_page = get_paginated_episodes(
        repo.repo_instance, podcast_id, page, per_page)

    return render_template(
        'podcastdescription.html',
        podcast=podcast,
        reviews=reviews,
        average_rating=average_rating,
        episodes=episodes,
        page=page,
        total_pages=total_pages,
        prev_page=prev_page,
        next_page=next_page,
        start_page=start_page,
        end_page=end_page
    )



@description_blueprint.route('/submit_review/<int:podcast_id>', methods=['POST'])
@login_required
def submit_review(podcast_id):
    rating = int(request.form['rating'])
    comment = request.form['comment']
    username = session['user_name']

    services.add_review(repo.repo_instance, podcast_id, comment, rating, username)

    return redirect(url_for('description_bp.show_podcast_description', podcast_id=podcast_id))

