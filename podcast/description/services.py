from datetime import datetime

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, User, Review

class NonExistentPodcastException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(repo: AbstractRepository, podcast_id: int, comment: str, rating: int, username: str):
    podcast = repo.get_podcast_by_id(podcast_id)
    if podcast is None:
        raise NonExistentPodcastException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create the review
    review_id = len(repo.get_reviews()) + 1
    review = Review(review_id, podcast, user, rating, comment)

    # Add review date
    # review.date = datetime.now()

    # Update repository
    repo.add_review(review)

    # Update podcast's review list
    podcast.add_review(review)


def get_podcast_by_id(repo, podcast_id):
    return repo.get_podcast_by_id(podcast_id)


def get_paginated_episodes(repo: AbstractRepository, podcast_id: int, page: int, per_page: int, page_window: int = 10):
    # Retrieve all episodes for the given podcast_id
    all_episodes = [episode for episode in repo.get_episodes() if episode.podcast.id == podcast_id]
    total_episodes = len(all_episodes)

    if total_episodes == 0:
        return [], 0, None, None, 1, 1  # No episodes, return an empty list

    total_pages = (total_episodes + per_page - 1) // per_page

    # Calculate start and end indices for the current page
    start = (page - 1) * per_page
    end = start + per_page

    # Get the episodes for the current page
    episodes = all_episodes[start:end]

    # Calculate previous and next page numbers
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    # Pagination window
    start_page = max(1, page - page_window // 2)
    end_page = min(start_page + page_window - 1, total_pages)

    # Adjust start_page if the window exceeds total_pages
    if end_page < total_pages:
        start_page = start_page
    else:
        start_page = max(1, total_pages - page_window + 1)

    return episodes, total_pages, prev_page, next_page, start_page, end_page


